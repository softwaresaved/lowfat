import copy

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import django.utils

from constance import config

from lowfat.management.commands import loadoldfunds
from lowfat.models import ApprovalChain, Blog, Claimant, Expense, Fund, FUND_STATUS_APPROVED_SET, FundSentMail
from lowfat.forms import FundForm, FundGDPRForm, FundImportForm, FundPublicForm, FundReviewForm
from lowfat.mail import fund_review_notification, new_fund_notification
from .claimant import get_terms_and_conditions_url

User = get_user_model()


@login_required
def fund_form(request, **kargs):  # pylint: disable=too-many-branches,too-many-statements
    if not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            claimant = None

    # Setup fund to edit if provide
    if "fund_id" in kargs:
        try:
            fund_to_edit = Fund.objects.get(id=kargs["fund_id"])
        except:  # pylint: disable=bare-except
            fund_to_edit = None
            messages.error(request, "The funding request that you want to edit doesn't exist.")
        if not (request.user.is_staff or
                claimant == fund_to_edit.claimant):
            fund_to_edit = None
            messages.error(request, "You don't have permission to edit the requested funding request.")
    else:
        fund_to_edit = None

    initial = {
        "start_date": django.utils.timezone.now(),
        "end_date": django.utils.timezone.now(),
    }

    if not request.user.is_staff:
        if claimant:
            initial["claimant"] = claimant
        else:
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
    elif request.GET.get("claimant_id"):
        initial["claimant"] = Claimant.objects.get(id=request.GET.get("claimant_id"))

    if fund_to_edit and claimant == fund_to_edit.claimant and fund_to_edit.status != 'U':
        formset = FundGDPRForm(
            request.POST or None,
            instance=fund_to_edit
        )
    else:
        formset = FundForm(
            request.POST or None,
            instance=fund_to_edit,
            initial=None if fund_to_edit else initial,
            is_staff=bool(request.user.is_staff)
        )

    if request.POST:
        # Handle submission
        if formset.is_valid():
            # Use Fellows approval chain for requests using this form
            formset.instance.approval_chain = ApprovalChain.FELLOWS

            fund = formset.save()
            messages.success(request, 'Funding request saved.')
            if not formset.cleaned_data["not_send_email_field"]:
                new_fund_notification(fund)

            fund.update_latlon()
            # Default value for budget_approved is budget_total.
            # The reason for this is to save staffs to copy and paste the approved amount.
            fund.budget_approved = fund.budget_total()
            fund.save()

            # Attempt to pre approved funding request.
            if fund.pre_approve():
                messages.success(request, 'Funding request approved.')
                if not formset.cleaned_data["not_send_email_field"]:
                    fund_review_notification(
                        "",
                        request.user,
                        fund,
                        fund,
                        True
                    )

            return HttpResponseRedirect(
                reverse('fund_detail', args=[fund.id,])
            )

    if not request.user.is_staff:
        formset.fields["claimant"].queryset = Claimant.objects.filter(user=request.user)
    elif request.GET.get("claimant_id"):
        formset.fields["claimant"].queryset = Claimant.objects.filter(id=request.GET.get("claimant_id"))
    else:
        formset.fields["claimant"].queryset = Claimant.objects.all()

    # Show submission form.
    context = {
        "title": "Edit funding request" if fund_to_edit else "Make a funding request",
        "terms_and_conditions_url": get_terms_and_conditions_url(request),
        "formset": formset,
        "js_files": ["js/request.js"],
    }
    return render(request, 'lowfat/form.html', context)


def fund_form_public(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('fund'))

    initial = {
        "start_date": django.utils.timezone.now(),
        "end_date": django.utils.timezone.now(),
    }

    formset = FundPublicForm(
        request.POST or None,
        initial=initial,
        is_staff=bool(request.user.is_superuser)
    )

    if request.POST and formset.is_valid():
        # Use One-Time approval chain for requests using this form
        formset.instance.approval_chain = ApprovalChain.ONE_TIME

        # Handle submission
        username = "{}.{}".format(
            formset.cleaned_data["forenames"].lower(),
            formset.cleaned_data["surname"].lower()
        )
        try:
            user = User.objects.get(username=username)
            is_new_user = False
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username,
                formset.cleaned_data["email"],
                User.objects.make_random_password(),
                first_name=formset.cleaned_data["forenames"],
                last_name=formset.cleaned_data["surname"]
            )
            user.save()
            is_new_user = True

        messages.success(request, 'Your username is {}.'.format(username))
        if is_new_user:
            claimant = Claimant.objects.create(
                user=user,
                forenames=formset.cleaned_data["forenames"],
                surname=formset.cleaned_data["surname"],
                email=formset.cleaned_data["email"],
                phone=formset.cleaned_data["phone"],
                home_city=formset.cleaned_data["home_city"]
            )
            claimant.save()
        else:
            claimant = Claimant.objects.get(
                user=user
            )

        fund = formset.save(commit=False)
        fund.claimant = claimant
        fund.new_access_token()
        fund.update_latlon()
        # Default value for budget_approved is budget_total.
        # The reason for this is to save staffs to copy and paste the approved amount.
        fund.budget_approved = fund.budget_total()
        fund.save()

        messages.success(request, 'Funding request saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_fund_notification(fund)

        return HttpResponseRedirect(
            reverse('fund_detail_public', args=[fund.access_token,])
        )

    # Show submission form.
    context = {
        "title": "Make a funding request",
        "terms_and_conditions_url": get_terms_and_conditions_url(request),
        "formset": formset,
        "js_files": ["js/request.js"],
    }
    return render(request, 'lowfat/form.html', context)


def _fund_detail(request, fund):
    # Setup query parameters
    funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPAMRF"
    expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"
    blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URGLPDO"

    context = {
        'funding_requests_status': funding_requests_status,
        'expenses_status': expenses_status,
        'blogs_status': blogs_status,
        'fund': fund,
        'expenses': Expense.objects.filter(
            fund=fund,
            status__in=expenses_status
        ),
        'blogs': Blog.objects.filter(
            fund=fund,
            status__in=blogs_status
        ),
        'emails': FundSentMail.objects.filter(fund=fund),
    }

    return render(request, 'lowfat/fund_detail.html', context)


def fund_detail_public(request, access_token):
    fund = Fund.objects.get(access_token=access_token)
    return _fund_detail(request, fund)


@login_required
def fund_detail(request, fund_id):
    fund = Fund.objects.get(id=fund_id)

    if request.user.is_staff:
        pass
    elif Claimant.objects.get(user=request.user) == fund.claimant:
        pass
    else:
        raise Http404("Funding request does not exist.")

    return _fund_detail(request, fund)


@staff_member_required
def fund_review(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)

    if request.POST:
        # Handle submission
        old_fund = copy.deepcopy(this_fund)
        formset = FundReviewForm(
            request.POST,
            instance=this_fund
        )

        if formset.is_valid():
            fund = formset.save()
            if fund.status in FUND_STATUS_APPROVED_SET and fund.approver == None:  # pylint: disable=singleton-comparison
                fund.approver = request.user
                fund.save()
                messages.success(request, 'Funding request updated.')
            if not formset.cleaned_data["not_send_email_field"]:
                fund_review_notification(
                    formset.cleaned_data['email'],
                    request.user,
                    old_fund,
                    fund,
                    not formset.cleaned_data['not_copy_email_field']
                )
            return HttpResponseRedirect(
                reverse('fund_detail', args=[fund.id,])
            )

    formset = FundReviewForm(
        None,
        instance=this_fund,
        is_staff=bool(request.user.is_staff)
    )

    context = {
        'fund': this_fund,
        'formset': formset,
        'emails': FundSentMail.objects.filter(fund=this_fund),
    }

    return render(request, 'lowfat/fund_review.html', context)


@login_required
def fund_edit(request, fund_id):
    if request.user.is_staff:  # pylint: disable=no-else-return
        return HttpResponseRedirect(
            reverse('admin:lowfat_fund_change', args=[fund_id,])
        )
    else:
        return fund_form(request, fund_id=fund_id)


@login_required
def fund_remove(request, fund_id):
    if request.user.is_staff:
        redirect_url = reverse('admin:lowfat_fund_delete', args=[fund_id,])
    else:
        if "next" in request.GET:
            redirect_url = request.GET["next"]
        else:
            redirect_url = "/"

        try:
            this_fund = Fund.objects.get(id=fund_id)
        except:  # pylint: disable=bare-except
            this_fund = None
            messages.error(request, "Funding request that you want to remove doesn't exist.")

        if this_fund and Claimant.objects.get(user=request.user) == this_fund.claimant:
            this_fund.remove()
            messages.success(request, 'Blog deleted with success.')
        else:
            messages.error(request, 'Only the claimant can remove the funding request.')

    return HttpResponseRedirect(redirect_url)


def fund_past(request):
    funds = Fund.objects.filter(
        start_date__lt=django.utils.timezone.now(),
        category="H",
        status__in=FUND_STATUS_APPROVED_SET,
        can_be_advertise_after=True,
    )

    context = {
        'funds': [(fund, Blog.objects.filter(
            fund=fund,
            status="P"
        )) for fund in funds],
    }

    return render(request, 'lowfat/fund_past.html', context)


def fund_ical(request, token):
    if token != config.CALENDAR_ACCESS_TOKEN:
        raise Http404("Expense claim does not exist.")

    funds = Fund.objects.filter(
        can_be_advertise_after=True,
    )

    context = {
        'funds': funds,
    }

    return render(request, 'lowfat/ical.html', context)


@staff_member_required
def fund_import(request):
    if request.POST:
        # Handle submission
        formset = FundImportForm(
            request.POST or None,
            request.FILES or None
        )

        if formset.is_valid():
            importer = loadoldfunds.Command()
            importer.handle({'csv': request.FILES['csv']})

            return HttpResponseRedirect(reverse('dashboard'))

    formset = FundImportForm()

    # Show submission form.
    context = {
        "title": "Import CSV",
        "formset": formset,
        "js_files": ["js/request.js"],
    }
    return render(request, 'lowfat/form.html', context)
