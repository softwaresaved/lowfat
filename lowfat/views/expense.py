import copy
import io
import shutil

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from PyPDF2 import PdfFileMerger, PdfFileReader

from lowfat.models import Claimant, Expense, Fund, FUND_STATUS_APPROVED_SET, ExpenseSentMail
from lowfat.forms import ExpenseForm, ExpenseReviewForm, ExpenseShortlistedForm
from lowfat.mail import expense_review_notification, new_expense_notification
from .claimant import get_terms_and_conditions_url


@login_required
def expense_form(request, **kargs):
    # Setup Expense to edit if provided
    expense_to_edit = None

    if "fund_id" in kargs and "expense_relative_number" in kargs:
        try:
            expense_to_edit = Expense.objects.get(
                fund__id=kargs["fund_id"],
                relative_number=kargs["expense_relative_number"]
            )

        except Expense.DoesNotExist:
            messages.error(request, "The expense that you want to edit doesn't exist.")

    # Setup Fund if provided
    fund_id = request.GET.get("fund_id")
    if fund_id:
        fund = Fund.objects.get(id=fund_id)
        initial = {"fund": fund}
    else:
        fund = None
        initial = {
            "amount_claimed": "0.00",  # Workaround for https://github.com/softwaresaved/lowfat/issues/191
        }

    try:
        claimant = Claimant.objects.get(user=request.user)

    except Claimant.DoesNotExist:
        claimant = None

    if claimant and not claimant.fellow:
        formset = ExpenseShortlistedForm(
            request.POST or None,
            request.FILES or None,
            instance=expense_to_edit,
            initial=None if expense_to_edit else initial,
            is_staff=bool(request.user.is_staff)
        )
    else:
        formset = ExpenseForm(
            request.POST or None,
            request.FILES or None,
            instance=expense_to_edit,
            initial=None if expense_to_edit else initial,
            is_staff=bool(request.user.is_staff)
        )

    if formset.is_valid():
        expense = formset.save()
        messages.success(request, 'Expense saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_expense_notification(expense)
        return HttpResponseRedirect(
            reverse('expense_detail_relative', args=[expense.fund.id, expense.relative_number])
        )

    # Limit dropdown list to claimant
    if fund_id:
        claimant = Claimant.objects.filter(id=fund.claimant.id)
    elif request.GET.get("claimant_id"):
        claimant = Claimant.objects.filter(id=request.GET.get("claimant_id"))
    elif request.user.is_staff:
        claimant = Claimant.objects.all()
    else:
        claimant = Claimant.objects.filter(user=request.user)
        if not claimant:
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
        formset.fields["fund"].queryset = Fund.objects.filter(
            claimant__in=claimant,
            status__in=FUND_STATUS_APPROVED_SET
        )

    # Show submission form.
    context = {
        "title": "Update expense claim" if expense_to_edit else "Submit expense claim",
        "terms_and_conditions_url": get_terms_and_conditions_url(request),
        "formset": formset,
    }
    return render(request, 'lowfat/form.html', context)


def expense_form_public(request, access_token):
    try:
        fund = Fund.objects.get(access_token=access_token)
        if not fund.access_token_is_valid():
            fund = None
    except ObjectDoesNotExist:
        fund = None

    if fund is None:
        raise Http404("Funding request does not exist.")

    initial = {"fund": fund}
    formset = ExpenseForm(
        request.POST or None,
        request.FILES or None,
        initial=initial,
        is_staff=bool(request.user.is_staff)
    )

    if formset.is_valid():
        expense = formset.save()
        expense.new_access_token()
        expense.save()
        messages.success(request, 'Expense saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_expense_notification(expense)
        return HttpResponseRedirect(
            reverse('expense_detail_public', args=[expense.access_token])
        )

    # Show submission form.
    context = {
        "title": "Submit expense claim",
        "terms_and_conditions_url": get_terms_and_conditions_url(request),
        "formset": formset,
    }
    return render(request, 'lowfat/form.html', context)


def _expense_detail(request, expense):
    if expense is None:
        raise Http404("Expense doesn't exist.")

    context = {
        'expense': expense,
        'emails': ExpenseSentMail.objects.filter(expense=expense),
    }

    return render(request, 'lowfat/expense_detail.html', context)


def expense_detail_public(request, access_token):
    try:
        expense = Expense.objects.get(access_token=access_token)
        if not expense.access_token_is_valid():
            expense = None
    except ObjectDoesNotExist:
        expense = None

    return _expense_detail(request, expense)


def expense_detail(request, expense_id):
    raise Http404("URL not supported in lowFAT 2.x.")


@login_required
def expense_detail_relative(request, fund_id, expense_relative_number):
    this_fund = Fund.objects.get(id=fund_id)
    this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)

    if not (request.user.is_staff or Claimant.objects.get(user=request.user) == this_expense.fund.claimant):
        this_expense = None

    return _expense_detail(request, this_expense)


@login_required
def expense_edit_relative(request, fund_id, expense_relative_number):
    if request.user.is_staff:  # pylint: disable=no-else-return
        this_expense = Expense.objects.get(
            fund__id=fund_id,
            relative_number=expense_relative_number
        )
        return HttpResponseRedirect(
            reverse('admin:lowfat_expense_change', args=[this_expense.id])
        )
    else:
        return expense_form(
            request,
            fund_id=fund_id,
            expense_relative_number=expense_relative_number
        )


@staff_member_required
def expense_review(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)

    if request.POST:
        # Handle submission
        old_expense = copy.deepcopy(this_expense)
        formset = ExpenseReviewForm(request.POST, instance=this_expense)

        if formset.is_valid():
            expense = formset.save()
            messages.success(request, 'Expense claim updated.')
            if not formset.cleaned_data["not_send_email_field"]:
                expense_review_notification(
                    formset.cleaned_data['email'],
                    request.user,
                    old_expense,
                    expense,
                    not formset.cleaned_data['not_copy_email_field']
                )

            if expense.status == 'A' and expense.final:
                expense.fund.status = 'F'
                expense.fund.save()
                messages.success(request, 'Funding request archived.')

            return HttpResponseRedirect(
                reverse('expense_detail_relative', args=[expense.fund.id, expense.relative_number])
            )

    formset = ExpenseReviewForm(
        None,
        instance=this_expense,
        is_staff=bool(request.user.is_staff)
    )

    context = {
        'expense': this_expense,
        'formset': formset,
        'emails': ExpenseSentMail.objects.filter(expense=this_expense),
    }

    return render(request, 'lowfat/expense_review.html', context)


@staff_member_required
def expense_review_relative(request, fund_id, expense_relative_number):
    this_fund = Fund.objects.get(id=fund_id)
    this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)
    return expense_review(request, this_expense.id)


@login_required
def expense_remove_relative(request, fund_id, expense_relative_number):
    try:
        this_fund = Fund.objects.get(id=fund_id)
        this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)
    except:  # pylint: disable=bare-except
        this_expense = None
        redirect_url = "/"
        messages.error(request, "The expense that you want to remove doesn't exist.")

    if this_expense:
        if request.user.is_staff:
            redirect_url = reverse('admin:lowfat_expense_delete', args=[this_expense.id])
        else:
            if "next" in request.GET:
                redirect_url = request.GET["next"]
            else:
                redirect_url = "/"

            if this_expense and Claimant.objects.get(user=request.user) == this_expense.fund.claimant:
                this_expense.remove()
                messages.success(request, 'Blog remove with success.')
            else:
                messages.error(request, 'Only the author can remove the blog.')

    return HttpResponseRedirect(redirect_url)


@login_required
def expense_append_relative(request, fund_id, expense_relative_number):
    try:
        this_expense = Expense.objects.get(
            fund=Fund.objects.get(id=fund_id),
            relative_number=expense_relative_number
        )
    except:  # pylint: disable=bare-except
        this_expense = None
        messages.error(request, "The expense that you want doesn't exist.")

    if request.POST and request.FILES and this_expense:
        try:
            # Workaround for 'bytes' object has no attribute 'seek'
            # Suggestion by ƘɌỈSƬƠƑ
            # https://stackoverflow.com/a/38678468/1802726
            request_pdf_io = io.BytesIO(request.FILES["pdf"].read())
            PdfFileReader(request_pdf_io)
            request_pdf_io.seek(0)
        except:  # pylint: disable=bare-except
            messages.error(request, 'File is not a PDF.')

        # Backup of original PDF
        shutil.copyfile(
            this_expense.claim.path,
            "{}-backup.pdf".format(this_expense.claim.path)
        )

        # Based on Emile Bergeron's suggestion
        # https://stackoverflow.com/a/29871560/1802726
        merger = PdfFileMerger()
        with open(this_expense.claim.path, "rb") as _file:
            # Workaround for 'bytes' object has no attribute 'seek'
            # Suggestion by ƘɌỈSƬƠƑ
            # https://stackoverflow.com/a/38678468/1802726
            original_pdf_io = io.BytesIO(_file.read())
            merger.append(original_pdf_io)
            merger.append(request_pdf_io)
            merger.write(this_expense.claim.path)

        messages.success(request, 'PDF updated.')

    return HttpResponseRedirect(
        reverse('expense_detail_relative', args=[fund_id, expense_relative_number])
    )


def _expense_claim(request, expense):
    if expense is None:
        raise Http404("PDF does not exist.")

    with open(expense.claim.path, "rb") as _file:
        response = HttpResponse(_file.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename="{}"'.format(
            expense.claim_clean_name())
    return response


def expense_claim(request, expense_id):
    raise Http404("URL not supported in lowFAT 2.x.")


@login_required
def expense_claim_relative(request, fund_id, expense_relative_number):
    try:
        fund = Fund.objects.get(id=fund_id)
        expense = Expense.objects.get(fund=fund, relative_number=expense_relative_number)

        if not (request.user.is_staff or Claimant.objects.get(
                user=request.user) == expense.fund.claimant):
            expense = None
    except ObjectDoesNotExist:
        expense = None

    return _expense_claim(request, expense)


def expense_claim_public(request, access_token):
    try:
        expense = Expense.objects.get(access_token=access_token)
        if not expense.access_token_is_valid():
            expense = None
    except ObjectDoesNotExist:
        expense = None

    return _expense_claim(request, expense)
