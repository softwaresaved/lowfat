import copy
import io
import logging
import shutil
import sys

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from PyPDF2 import PdfMerger
from PyPDF2.errors import PdfReadError

from lowfat.models import Claimant, Expense, Fund, FUND_STATUS_APPROVED_SET, ExpenseSentMail
from lowfat.forms import ExpenseForm, ExpenseReviewForm, ExpenseShortlistedForm
from lowfat.mail import expense_review_notification, new_expense_notification
from .claimant import get_terms_and_conditions_url

from .base import FileFieldView, OwnerStaffOrTokenMixin

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


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
        formset = ExpenseReviewForm(request.POST,
                                    request.FILES or None,
                                    instance=this_expense)

        if formset.is_valid():
            expense = formset.save()
            messages.success(request, 'Expense claim updated.')
            if not formset.cleaned_data["not_send_email_field"]:
                expense_review_notification(
                    request,
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

    except:
        logger.warning('Exception caught by bare except')
        logger.warning('%s %s', *(sys.exc_info()[0:2]))

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
def expense_append_relative(request, fund_id: int, expense_relative_number: int):
    """Append pages to the expense receipts PDF.

    Expects POST request containing a PDF to append.
    """
    fund = get_object_or_404(Fund, id=fund_id)
    this_expense = get_object_or_404(Expense,
                                     fund=fund,
                                     relative_number=expense_relative_number)

    if request.POST and request.FILES:
        # Backup of original PDF
        shutil.copyfile(
            this_expense.receipts.path,
            f"{this_expense.receipts.path}-backup.pdf"
        )

        # Based on Emile Bergeron's suggestion
        # https://stackoverflow.com/a/29871560/1802726
        merger = PdfMerger()
        try:
            with open(this_expense.receipts.path, "rb") as _file:
                # Files need to be cast as `BytesIO` to provide `.seek()`
                # https://stackoverflow.com/a/38678468/1802726
                original_pdf_io = io.BytesIO(_file.read())
                request_pdf_io = io.BytesIO(request.FILES["pdf"].read())
                merger.append(original_pdf_io)
                merger.append(request_pdf_io)
                merger.write(this_expense.receipts.path)

                messages.success(request, 'Receipts PDF updated.')

        except PdfReadError:
            messages.error(request, 'Uploaded file is not a PDF.')

    return HttpResponseRedirect(
        reverse('expense_detail_relative', args=[fund_id, expense_relative_number])
    )


class ExpenseClaimView(OwnerStaffOrTokenMixin, FileFieldView):
    """Download an expense claim form document."""
    model = Expense
    field_name = "claim"
    owner_field = "fund.claimant.user"

    def get_object(self, queryset=None):
        if "token" in self.kwargs:
            return get_object_or_404(self.model,
                                     access_token=self.kwargs["access_token"])

        return get_object_or_404(
            self.model,
            fund=self.kwargs["fund_id"],
            relative_number=self.kwargs["expense_relative_number"])


class ExpenseReceiptsView(OwnerStaffOrTokenMixin, FileFieldView):
    """Download an expense claim receipts document."""
    model = Expense
    field_name = "receipts"
    owner_field = "fund.claimant.user"

    def get_object(self, queryset=None):
        if "token" in self.kwargs:
            return get_object_or_404(self.model,
                                     access_token=self.kwargs["access_token"])

        return get_object_or_404(
            self.model,
            fund=self.kwargs["fund_id"],
            relative_number=self.kwargs["expense_relative_number"])


class ExpenseSupportingDocsView(OwnerStaffOrTokenMixin, FileFieldView):
    """Download supporting documents for the expenses claim."""
    model = Expense
    field_name = "supporting_docs"
    owner_field = "fund.claimant.user"

    def get_object(self, queryset=None):
        if "token" in self.kwargs:
            return get_object_or_404(self.model,
                                     access_token=self.kwargs["access_token"])

        return get_object_or_404(
            self.model,
            fund=self.kwargs["fund_id"],
            relative_number=self.kwargs["expense_relative_number"])
        

class ExpenseFinalClaimFormView(OwnerStaffOrTokenMixin, FileFieldView):
    """Download final claim form."""
    model = Expense
    field_name = "upload_final_claim_form"
    owner_field = "fund.claimant.user"

    def get_object(self, queryset=None):
        if "token" in self.kwargs:
            return get_object_or_404(self.model,
                                     access_token=self.kwargs["access_token"])

        return get_object_or_404(
            self.model,
            fund=self.kwargs["fund_id"],
            relative_number=self.kwargs["expense_relative_number"])