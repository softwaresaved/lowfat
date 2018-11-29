import copy
import io
import os
import shutil

import django.utils
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render

from constance import config

from PyPDF2 import PdfFileMerger, PdfFileReader

from .management.commands import loadoldfunds as loadoldfunds
from .models import *
from .forms import *
from .mail import *

def get_terms_and_conditions_url(request):
    """Return the terms and conditions link associated with the user."""
    url = TermsAndConditions.objects.get(
        year=str(django.utils.timezone.now().year)
    ).url
    if not request.user.is_superuser and not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
            url = claimant.terms_and_conditions.url
        except:  # pylint: disable=bare-except
            pass

    return url

def index(request):
    context = {
        'claimants': Claimant.objects.filter(
            Q(fellow=True) | Q(collaborator=True)
        ),
        'funds': [(fund, Blog.objects.filter(
            fund=fund,
            status="P"
        )) for fund in Fund.objects.filter(category="H", start_date__gte=django.utils.timezone.now(), can_be_advertise_before=True)],
    }

    return render(request, 'lowfat/index.html', context)

@login_required
def dashboard(request):
    context = {
        'ical_token': config.CALENDAR_ACCESS_TOKEN,
    }

    if not request.user.is_superuser and not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/welcome/'}))

        # Setup query parameters
        funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPARF"  # Pending
        expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"  # All
        blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URCGLPMDOX"  # All

        context.update(
            {
                'funding_requests_status': funding_requests_status,
                'expenses_status': expenses_status,
                'blogs_status': blogs_status,
                'claimant': claimant,
                'budget_available': claimant.claimantship_available(),
                'funds': pair_fund_with_blog(
                    Fund.objects.filter(
                        claimant=claimant,
                        status__in=funding_requests_status
                    ),
                    "P"
                ),
                'expenses': Expense.objects.filter(
                    fund__claimant=claimant,
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(Q(author=claimant, status__in=blogs_status) | Q(coauthor=claimant, status__in=blogs_status)),
            }
        )
    else:
        # Setup query parameters
        funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UP"  # Pending
        expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCP"  # Pending
        blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URCGL"  # Pending

        context.update(
            {
                'funding_requests_status': funding_requests_status,
                'expenses_status': expenses_status,
                'blogs_status': blogs_status,
                'funds': pair_fund_with_blog(
                    Fund.objects.filter(
                        status__in=funding_requests_status
                    ),
                    "P"
                ),
                'expenses': Expense.objects.filter(
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(
                    status__in=blogs_status
                ),
            }
        )

    return render(request, 'lowfat/dashboard.html', context)

@staff_member_required
def search(request):
    search_text = request.POST.get("search")
    context = {
        "search": search_text,
        "fellows": Claimant.objects.filter(
            (Q(forenames__contains=search_text) |
             Q(surname__contains=search_text) |
             Q(email__contains=search_text) |
             Q(research_area__contains=search_text) |
             Q(affiliation__contains=search_text) |
             Q(work_description__contains=search_text) |
             Q(website__contains=search_text) |
             Q(github__contains=search_text) |
             Q(twitter__contains=search_text)) &
            (Q(fellow=True) | Q(collaborator=True))
        ),
        "claimants": Claimant.objects.filter(
            (Q(forenames__contains=search_text) |
             Q(surname__contains=search_text) |
             Q(email__contains=search_text) |
             Q(research_area__contains=search_text) |
             Q(affiliation__contains=search_text) |
             Q(work_description__contains=search_text) |
             Q(website__contains=search_text) |
             Q(github__contains=search_text) |
             Q(twitter__contains=search_text)) &
            Q(fellow=False)
        ),
        "funds": Fund.objects.filter(
            Q(claimant__forenames__contains=search_text) |
            Q(claimant__surname__contains=search_text) |
            Q(title__contains=search_text) |
            Q(url__contains=search_text) |
            Q(justification__contains=search_text) |
            Q(additional_info__contains=search_text)
        ),
    }

    return render(request, 'lowfat/search.html', context)

@staff_member_required
def promote(request):
    context = {
        "claimants": Claimant.objects.filter(),
    }

    return render(request, 'lowfat/promote.html', context)


@login_required
def claimant_form(request):
    if not request.user.is_superuser and not request.user.is_staff:
        instance = Claimant.objects.get(user=request.user)
        title_begin = "Edit"
    else:
        instance = None
        title_begin = "Create"

    if "full" in request.GET:
        formset = FellowForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "fellow"
    else:
        formset = ClaimantForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "claimant"

    if formset.is_valid():
        claimant = formset.save()
        claimant.update_latlon()
        messages.success(request, 'Profile saved.')
        return HttpResponseRedirect(reverse('claimant_detail',
                                            args=[claimant.id,]))

    # Show submission form.
    context = {
        "title": "{} {}".format(title_begin, title_end),
        "formset": formset,
        "submit_text": "Save" if instance is None else "Update",
    }
    return render(request, 'lowfat/form.html', context)

# pylint: disable=unused-argument
@staff_member_required
def claimant_promote(request, claimant_id):
    claimant = Claimant.objects.get(id=claimant_id)
    claimant.slected = True
    claimant.save()

    return HttpResponseRedirect(
        reverse('claimant_detail', args=[claimant.id,])
    )

def claimant_detail(request, claimant_id):
    """Details about claimant."""
    this_claimant = Claimant.objects.get(id=claimant_id)

    # Avoid leak information from applicants
    if not request.user.is_superuser and not request.user.is_staff and not (this_claimant.fellow or this_claimant.received_offer or this_claimant.shortlisted or this_claimant.collaborator):
        raise Http404("Claimant does not exist.")

    # Setup query parameters
    funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPARF"
    expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"
    blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URGLPDO"

    context = {
        'funding_requests_status': funding_requests_status,
        'expenses_status': expenses_status,
        'blogs_status': blogs_status,
        'claimant': this_claimant,
    }

    if request.user.is_staff:
        funds = Fund.objects.filter(
            claimant=this_claimant,
            status__in=funding_requests_status
        )
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
                'expenses': Expense.objects.filter(
                    fund__claimant=this_claimant,
                    status__in=expenses_status
                ),
                'blogs': Blog.objects.filter(
                    Q(author=this_claimant, status__in=blogs_status) | Q(coauthor=this_claimant, status__in=blogs_status)
                ).distinct(),
            }
        )
    else:
        funds = Fund.objects.filter(
            claimant=this_claimant,
            can_be_advertise_after=True,
            status__in="AF"
        )
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
                'blogs': Blog.objects.filter(
                    Q(author=this_claimant, status="P") | Q(coauthor=this_claimant, status="P")
                ).distinct(),
            }
        )

    return render(request, 'lowfat/claimant_detail.html', context)

def claimant_slug_resolution(request, claimant_slug):
    """Resolve claimant slug and return the details."""
    try:
        claimant = Claimant.objects.get(Q(slug=claimant_slug) & (Q(fellow=True) | Q(collaborator=True) | Q(received_offer=True)))
    except:  # pylint: disable=bare-except
        claimant = None

    if claimant:
        return claimant_detail(request, claimant.id)

    raise Http404("Claimant does not exist.")

@login_required
def my_profile(request):
    if not request.user.is_superuser and not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))

        return claimant_detail(request, claimant.id)

    raise Http404("Claimant does not exist.")

@login_required
def fund_form(request, **kargs):  # pylint: disable=too-many-branches
    # Setup fund to edit if provide
    if "fund_id" in kargs:
        try:
            fund_to_edit = Fund.objects.get(id=kargs["fund_id"])
        except:  # pylint: disable=bare-except
            fund_to_edit = None
            messages.error(request, "The funding request that you want to edit doesn't exist.")
        if not (request.user.is_superuser or
                Claimant.objects.get(user=request.user) == fund_to_edit.claimant):
            fund_to_edit = None
            messages.error(request, "You don't have permission to edit the requested funding request.")
    else:
        fund_to_edit = None

    initial = {
        "start_date": django.utils.timezone.now(),
        "end_date": django.utils.timezone.now(),
    }

    if not request.user.is_staff:
        try:
            initial["claimant"] = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
    elif request.GET.get("claimant_id"):
        initial["claimant"] = Claimant.objects.get(id=request.GET.get("claimant_id"))

    if fund_to_edit and Claimant.objects.get(user=request.user) == fund_to_edit.claimant and fund_to_edit.status != 'U':
        formset = FundGDPRForm(
            request.POST or None,
            instance=fund_to_edit
        )
    else:
        formset = FundForm(
            request.POST or None,
            instance=fund_to_edit,
            initial=None if fund_to_edit else initial,
            is_staff=True if request.user.is_superuser else False
        )

    if request.POST:
        # Handle submission
        if formset.is_valid():
            fund = formset.save()
            fund.update_latlon()
            messages.success(request, 'Funding request saved.')
            if not formset.cleaned_data["not_send_email_field"]:
                new_fund_notification(fund)

            # Default value for budget_approved is budget_total.
            # The reason for this is to save staffs to copy and paste the approved amount.
            fund.budget_approved = fund.budget_total()
            fund.save()

            return HttpResponseRedirect(
                reverse('fund_detail', args=[fund.id,])
            )

    if type(formset).__name__ == "FundForm":
        if not request.user.is_superuser:
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

@login_required
def fund_detail(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_fund.claimant):

        # Setup query parameters
        funding_requests_status = request.GET["funding_requests"] if "funding_requests" in request.GET else "UPARF"
        expenses_status = request.GET["expenses"] if "expenses" in request.GET else "WSCPAF"
        blogs_status = request.GET["blogs"] if "blogs" in request.GET else "URGLPDO"

        context = {
            'funding_requests_status': funding_requests_status,
            'expenses_status': expenses_status,
            'blogs_status': blogs_status,
            'fund': this_fund,
            'expenses': Expense.objects.filter(
                fund=this_fund,
                status__in=expenses_status
            ),
            'blogs': Blog.objects.filter(
                fund=this_fund,
                status__in=blogs_status
            ),
            'emails': FundSentMail.objects.filter(fund=this_fund),
        }

        return render(request, 'lowfat/fund_detail.html', context)

    raise Http404("Funding request does not exist.")

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
            if fund.status == "A" and fund.approver == None:
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
        is_staff=True if request.user.is_superuser else False
    )

    context = {
        'fund': this_fund,
        'formset': formset,
        'emails': FundSentMail.objects.filter(fund=this_fund),
    }

    return render(request, 'lowfat/fund_review.html', context)

@login_required
def fund_edit(request, fund_id):
    if request.user.is_superuser:  # pylint: disable=no-else-return
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
        status__in=["A", "F"],
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

@login_required
def expense_form(request, **kargs):
    # Setup Expense to edit if provide
    if "fund_id" in kargs and "expense_relative_number" in kargs:
        try:
            expense_to_edit = Expense.objects.get(
                fund__id=kargs["fund_id"],
                relative_number=kargs["expense_relative_number"]
            )
        except:  # pylint: disable=bare-except
            expense_to_edit = None
            messages.error(request, "The expense that you want to edit doesn't exist.")
    else:
        expense_to_edit = None

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
    except:  # pylint: disable=bare-except
        claimant = None
    if claimant and not claimant.fellow:
        formset = ExpenseShortlistedForm(
            request.POST or None,
            request.FILES or None,
            instance=expense_to_edit,
            initial=None if expense_to_edit else initial,
            is_staff=True if request.user.is_superuser else False
        )
    else:
        formset = ExpenseForm(
            request.POST or None,
            request.FILES or None,
            instance=expense_to_edit,
            initial=None if expense_to_edit else initial,
            is_staff=True if request.user.is_superuser else False
        )

    if formset.is_valid():
        expense = formset.save()
        messages.success(request, 'Expense saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_expense_notification(expense)
        return HttpResponseRedirect(
            reverse('expense_detail', args=[expense.id,])
        )

    # Limit dropdown list to claimant
    if fund_id:
        claimant = Claimant.objects.filter(id=fund.claimant.id)
    elif request.GET.get("claimant_id"):
        claimant = Claimant.objects.filter(id=request.GET.get("claimant_id"))
    elif request.user.is_superuser:
        claimant = Claimant.objects.all()
    else:
        claimant = Claimant.objects.filter(user=request.user)
        if not claimant:
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
    formset.fields["fund"].queryset = Fund.objects.filter(
        claimant__in=claimant,
        status__in=['A']
    )

    # Show submission form.
    context = {
        "title": "Update expense claim" if expense_to_edit else "Submit expense claim",
        "terms_and_conditions_url": get_terms_and_conditions_url(request),
        "formset": formset,
    }
    return render(request, 'lowfat/form.html', context)

@login_required
def expense_detail(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_expense.fund.claimant):
        context = {
            'expense': Expense.objects.get(id=expense_id),
            'emails': ExpenseSentMail.objects.filter(expense=this_expense),
        }

        return render(request, 'lowfat/expense_detail.html', context)

    raise Http404("Expense claim does not exist.")

@login_required
def expense_detail_relative(request, fund_id, expense_relative_number):
    this_fund = Fund.objects.get(id=fund_id)
    this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)
    return expense_detail(request, this_expense.id)

@login_required
def expense_edit_relative(request, fund_id, expense_relative_number):
    if request.user.is_superuser:  # pylint: disable=no-else-return
        this_expense = Expense.objects.get(
            fund__id=fund_id,
            relative_number=expense_relative_number
        )
        return HttpResponseRedirect(
            reverse('admin:lowfat_expense_change', args=[this_expense.id,])
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
                reverse('expense_detail_relative', args=[expense.fund.id, expense.relative_number,])
            )

    formset = ExpenseReviewForm(
        None,
        instance=this_expense,
        is_staff=True if request.user.is_superuser else False
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
            redirect_url = reverse('admin:lowfat_expense_delete', args=[this_expense.id,])
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
        except:
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
        reverse('expense_detail_relative', args=[fund_id, expense_relative_number,])
    )

@login_required
def expense_claim(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_expense.fund.claimant):
        with open(this_expense.claim.path, "rb") as _file:
            response = HttpResponse(_file.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename="{}"'.format(
                this_expense.claim_clean_name())
            return response

    raise Http404("PDF does not exist.")

@login_required
def expense_claim_relative(request, fund_id, expense_relative_number):
    this_fund = Fund.objects.get(id=fund_id)
    this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)
    return expense_claim(request, this_expense.id)

@login_required
def blog_form(request, **kargs):
    # Setup Blog to edit if provide
    if "blog_id" in kargs:
        try:
            blog_to_edit = Blog.objects.get(id=kargs["blog_id"])
        except:  # pylint: disable=bare-except
            blog_to_edit = None
            messages.error(request, "The blog that you want to edit doesn't exist.")
    else:
        blog_to_edit = None
    # Setup Fund if provided
    fund_id = request.GET.get("fund_id")
    if fund_id:
        fund = Fund.objects.get(id=fund_id)
        initial = {"fund": fund}
    else:
        fund = None
        initial = {}

    formset = BlogForm(
        request.POST or None,
        request.FILES or None,
        instance=blog_to_edit,
        initial=None if blog_to_edit else initial,
        is_staff=True if request.user.is_superuser else False
    )

    if formset.is_valid():
        blog = formset.save()

        # Handle blog post not related with a funding request
        if not blog.author:
            if formset.cleaned_data["author"]:  # Because blog.author is None!
                blog.author = Claimant.objects.get(id=formset.cleaned_data["author"])
            elif blog.fund:
                blog.author = blog.fund.claimant
            elif not request.user.is_superuser:
                blog.author = Claimant.objects.get(user=request.user)
            else:
                blog.delete()  # XXX Quick way to solve the issue
                messages.error(request, 'Blog post not saved. Please provide a author.')
                return HttpResponseRedirect(
                    reverse('blog')
                )
        blog.save()

        messages.success(request, 'Blog draft saved.')
        if not formset.cleaned_data["not_send_email_field"]:
            new_blog_notification(blog)
        return HttpResponseRedirect(
            reverse('blog_detail', args=[blog.id,])
        )

    # Limit dropdown list to claimant
    if not request.user.is_superuser:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/unavailable/'}))
        formset.fields["fund"].queryset = Fund.objects.filter(
            claimant=claimant,
            status__in=['A']
        )
    elif request.GET.get("claimant_id"):
        claimant = Claimant.objects.get(id=request.GET.get("claimant_id"))
        formset.fields["fund"].queryset = Fund.objects.filter(
            claimant=claimant,
            status__in=['A']
        )

    # Show submission form.
    context = {
        "title": "Edit blog post draft" if blog_to_edit else "Submit blog post draft",
        "formset": formset,
        "js_files": ["js/blog.js"],
    }
    return render(request, 'lowfat/form.html', context)

@login_required
def blog_detail(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_blog.author or
            Claimant.objects.get(user=request.user) in this_blog.coauthor.all()):
        context = {
            'blog': Blog.objects.get(id=blog_id),
            'emails': BlogSentMail.objects.filter(blog=this_blog),
        }

        return render(request, 'lowfat/blog_detail.html', context)

    raise Http404("Blog post does not exist.")

@login_required
def blog_edit(request, blog_id):
    if request.user.is_superuser:  # pylint: disable=no-else-return
        return HttpResponseRedirect(
            reverse('admin:lowfat_blog_change', args=[blog_id,])
        )
    else:
        return blog_form(request, blog_id=blog_id)

@staff_member_required
def blog_review(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if request.POST:
        # Handle submission
        old_blog = copy.deepcopy(this_blog)
        formset = BlogReviewForm(request.POST, instance=this_blog)

        if formset.is_valid():
            blog = formset.save()
            messages.success(request, 'Blog updated.')
            if not formset.cleaned_data["not_send_email_field"]:
                blog_review_notification(
                    formset.cleaned_data['email'],
                    request.user,
                    old_blog,
                    blog,
                    not formset.cleaned_data['not_copy_email_field']
                )
            return HttpResponseRedirect(
                reverse('blog_detail', args=[blog.id,])
            )

    formset = BlogReviewForm(
        None,
        instance=this_blog,
        is_staff=True if request.user.is_superuser else False
    )

    # Limit dropdown list to staffs
    if not this_blog.reviewer:
        formset.fields["reviewer"].queryset = User.objects.filter(is_staff=True)

    context = {
        'blog': this_blog,
        'emails': BlogSentMail.objects.filter(blog=this_blog),
        'formset': formset,
    }

    return render(request, 'lowfat/blog_review.html', context)

@login_required
def blog_remove(request, blog_id):
    if request.user.is_staff:
        redirect_url = reverse('admin:lowfat_blog_delete', args=[blog_id,])
    else:
        if "next" in request.GET:
            redirect_url = request.GET["next"]
        else:
            redirect_url = "/"

        try:
            this_blog = Blog.objects.get(id=blog_id)
        except:  # pylint: disable=bare-except
            this_blog = None
            messages.error(request, "The blog that you want to remove doesn't exist.")

        if this_blog and Claimant.objects.get(user=request.user) == this_blog.author:
            this_blog.remove()
            messages.success(request, 'Blog deleted with success.')
        else:
            messages.error(request, 'Only the author can remove the blog.')

    return HttpResponseRedirect(redirect_url)

@staff_member_required
def recent_actions(request):
    """Recent actions view."""
    action_list = []
    action_list.extend([(claimant.history_date, claimant) for claimant in Claimant.history.all()])  # pylint: disable=E1101
    action_list.extend([(fund.history_date, fund) for fund in Fund.history.all()])  # pylint: disable=E1101
    action_list.extend([(expense.history_date, expense) for expense in Expense.history.all()])  # pylint: disable=E1101
    action_list.extend([(blog.history_date, blog) for blog in Blog.history.all()])  # pylint: disable=E1101

    action_list.sort(key=lambda x: x[0], reverse=True)
    paginator = Paginator([action[1] for action in action_list], 10)

    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)

    context = {
        "actions": actions,
    }

    return render(request, "lowfat/recent_actions.html", context)

@staff_member_required
def report_by_name(request, report_filename):
    """Report view."""
    try:
        with open("lowfat/reports/html/{}".format(report_filename), "r") as _file:
            response = HttpResponse(_file.read(), content_type="text/plain")
            return response
    except:  # pylint: disable=bare-except
        raise Http404("Report does not exist.")

@staff_member_required
def report(request):
    """Report view."""
    context = {
        'notebook_filenames': [filename for filename in os.listdir("lowfat/reports/html/") if filename.endswith(".html")],
    }

    return render(request, 'lowfat/report.html', context)

@staff_member_required
def geojson(request):
    """Return the GeoJSON file."""

    context = {
        'claimants': Claimant.objects.all(),
        'funds': Fund.objects.all(),
    }

    return render(request, 'lowfat/map.geojson', context)
