import django.utils
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from bokeh.charts import Bar, Histogram
from bokeh.embed import components
from bokeh.resources import CDN

from .management.commands import loadoldfunds as loadoldfunds
from .models import *
from .forms import *
from .mail import *

def index(request):
    context = {
        'claimants': Claimant.objects.exclude(selected=False).order_by('application_year').reverse(),
        'funds': Fund.objects.filter(category="H", start_date__gte=django.utils.timezone.now(), can_be_advertise_before=True).order_by("start_date").reverse(),
    }

    if request.user.is_authenticated() and request.user.is_superuser:
        context.update(
            {
                'show_grant_available': True,
            }
        )

    return render(request, 'lowfat/index.html', context)

@login_required
def dashboard(request):
    context = {}

    if not request.user.is_superuser and not request.user.is_staff:
        try:
            claimant = Claimant.objects.get(user=request.user)
        except:  # pylint: disable=bare-except
            return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': '/welcome/'}))

        funds = Fund.objects.filter(claimant=claimant).reverse()

        context.update(
            {
                'claimant': claimant,
                'budget_available': claimant.claimantship_available(),
                'funds': pair_fund_with_blog(funds, "P"),
                'expenses': Expense.objects.filter(fund__claimant=claimant).reverse(),
                'blogs': Blog.objects.filter(fund__claimant=claimant).reverse(),
            }
        )
    else:
        if "funding_requests" in request.GET:
            funding_requests_status = request.GET["funding_requests"]
        else:
            funding_requests_status = "UP"

        if "expenses" in request.GET:
            expenses_status = request.GET["expenses"]
        else:
            expenses_status = "WSC"

        if "blogs" in request.GET:
            blogs_status = request.GET["blogs"]
        else:
            blogs_status = "UR"

        context.update(
            {
                'funds': Fund.objects.filter(status__in=funding_requests_status).reverse(),
                'expenses': Expense.objects.filter(status__in=expenses_status).reverse(),
                'blogs': Blog.objects.filter(status__in=blogs_status).reverse(),
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
            Q(selected=True)
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
            Q(selected=False)
        ),
        "funds": Fund.objects.filter(
            Q(claimant__forenames__contains=search_text) |
            Q(claimant__surname__contains=search_text) |
            Q(name__contains=search_text) |
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

    # pylint: disable=redefined-variable-type
    if "full" in request.GET:
        formset = FellowForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "fellow"
    else:
        formset = ClaimantForm(request.POST or None, request.FILES or None, instance=instance)
        title_end = "claimant"

    if formset.is_valid():
        claimant = formset.save()
        messages.success(request, 'Profile saved on our database.')
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

    if not request.user.is_superuser and not request.user.is_staff and not this_claimant.selected:
        raise Http404("Claimant does not exist.")

    context = {
        'claimant': this_claimant,
        'blogs': Blog.objects.filter(
            fund__claimant=this_claimant,
        ),
    }

    if request.user.is_authenticated() and (request.user.is_superuser or
                                            this_claimant.user == request.user):
        funds = Fund.objects.filter(claimant=this_claimant)
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
                'expenses': Expense.objects.filter(fund__claimant=this_claimant),
                'show_finances': True,
            }
        )
    else:
        funds = Fund.objects.filter(
            claimant=this_claimant,
            can_be_advertise_after=True,
            status__in=["A", "F"]
        )
        context.update(
            {
                'funds': pair_fund_with_blog(funds, "P"),
            }
        )

    return render(request, 'lowfat/claimant_detail.html', context)

def claimant_slug_resolution(request, claimant_slug):
    """Resolve claimant slug and return the details."""
    try:
        claimant = Claimant.objects.get(slug=claimant_slug, selected=True)
    except:  # pylint: disable=bare-except
        claimant = None

    if claimant:
        return claimant_detail(request, claimant.id)

    raise Http404("Claimant does not exist.")

@login_required
def my_profile(request):
    if not request.user.is_superuser and not request.user.is_staff:
        claimant = Claimant.objects.get(user=request.user)
        return claimant_detail(request, claimant.id)

    raise Http404("Claimant does not exist.")

@login_required
def fund_form(request):
    if request.POST:
        # Handle submission
        post = request.POST.copy()
        claimant = Claimant.objects.get(id=post['claimant'])
        post['claimant'] = claimant.id
        formset = FundForm(post)

        if formset.is_valid():
            fund = formset.save()

            # Default value for budget_approved is budget_total.
            # The reason for this is to save staffs to copy and paste the approved amount.
            fund.budget_approved = fund.budget_total()
            fund.save()
            messages.success(request, 'Funding request saved on our database.')

            # FIXME Enable this in the future.
            # new_fund_notification(fund)
            return HttpResponseRedirect(
                reverse('fund_detail', args=[fund.id,])
            )

    initial = {
        "start_date": django.utils.timezone.now(),
        "end_date": django.utils.timezone.now(),
    }

    if not request.user.is_superuser:
        initial["claimant"] = Claimant.objects.get(user=request.user)
    elif request.GET.get("claimant_id"):
        initial["claimant"] = Claimant.objects.get(id=request.GET.get("claimant_id"))

    formset = FundForm(initial=initial)

    if not request.user.is_superuser:
        formset.fields["claimant"].queryset = Claimant.objects.filter(user=request.user)
    elif request.GET.get("claimant_id"):
        formset.fields["claimant"].queryset = Claimant.objects.filter(id=request.GET.get("claimant_id"))
    else:
        formset.fields["claimant"].queryset = Claimant.objects.all().order_by("forenames")

    # Show submission form.
    context = {
        "title": "Make a funding request",
        "formset": formset,
        "js_files": ["js/request.js"],
    }
    return render(request, 'lowfat/form.html', context)

@login_required
def fund_detail(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_fund.claimant):

        context = {
            'fund': this_fund,
            'expenses': Expense.objects.filter(fund=this_fund),
            'blogs': Blog.objects.filter(fund=this_fund),
            'emails': FundSentMail.objects.filter(fund=this_fund),
        }

        return render(request, 'lowfat/fund_detail.html', context)

    raise Http404("Fund does not exist.")

@staff_member_required
def fund_review(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)

    if request.POST:
        # Handle submission
        formset = FundReviewForm(request.POST, instance=this_fund)

        if formset.is_valid():
            fund = formset.save()
            mail = FundSentMail(
                **{
                    "justification": formset.cleaned_data['email'],
                    "sender": request.user,
                    "receiver": fund.claimant,
                    "fund": fund,
                }
            )
            mail.save()
            # FIXME Enable this in the future.
            # fund_review_notification(mail)
            return HttpResponseRedirect(
                reverse('fund_detail', args=[fund.id,])
            )

    formset = FundReviewForm(None, instance=this_fund)

    context = {
        'fund': this_fund,
        'formset': formset,
        'emails': FundSentMail.objects.filter(fund=this_fund),
    }

    return render(request, 'lowfat/fund_review.html', context)

def fund_past(request):
    funds = Fund.objects.filter(
        start_date__lt=django.utils.timezone.now(),
        category="H",
        status__in=["A", "F"],
        can_be_advertise_after=True,
    ).order_by("start_date").reverse()

    context = {
        'funds': [(fund, Blog.objects.filter(
            fund=fund,
            status="P"
        )) for fund in funds],
    }

    return render(request, 'lowfat/fund_past.html', context)

@staff_member_required
def fund_import(request):
    if request.POST:
        # Handle submission
        formset = FundImportForm(request.POST or None, request.FILES or None)

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
def expense_form(request):
    # Setup Fund if provided
    fund_id = request.GET.get("fund_id")
    if fund_id:
        fund = Fund.objects.get(id=fund_id)
        initial = {"fund": fund}
    else:
        fund = None
        initial = {}

    formset = ExpenseForm(request.POST or None, request.FILES or None, initial=initial)

    if formset.is_valid():
        expense = formset.save()
        messages.success(request, 'Expense saved on our database.')
        # FIXME Enable this in the future.
        # new_expense_notification(expense)
        return HttpResponseRedirect(
            reverse('expense_detail', args=[expense.id,])
        )

    # Limit dropdown list to claimant
    if fund_id:
        claimant = fund.claimant
    elif request.GET.get("claimant_id"):
        claimant = Claimant.objects.get(id=request.GET.get("claimant_id"))
    elif request.user.is_superuser:
        claimant = Claimant.objects.all()
    else:
        claimant = Claimant.objects.get(user=request.user)
    formset.fields["fund"].queryset = Fund.objects.filter(
        claimant=claimant,
        status__in=['A']
    )

    # Show submission form.
    context = {
        "title": "Submit expense claim",
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

@staff_member_required
def expense_review(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)

    if request.POST:
        # Handle submission
        formset = ExpenseReviewForm(request.POST, instance=this_expense)

        if formset.is_valid():
            expense = formset.save()
            mail = ExpenseSentMail(
                **{
                    "justification": formset.cleaned_data['email'],
                    "sender": request.user,
                    "receiver": expense.fund.claimant,
                    "expense": expense,
                }
            )
            mail.save()
            # FIXME Enable this in the future.
            # expense_review_notification(mail)
            return HttpResponseRedirect(
                reverse('expense_detail', args=[expense.id,])
            )

    formset = ExpenseReviewForm(None, instance=this_expense)

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
def blog_form(request):
    # Setup Fund if provided
    fund_id = request.GET.get("fund_id")
    if fund_id:
        fund = Fund.objects.get(id=fund_id)
        initial = {"fund": fund}
    else:
        fund = None
        initial = {}

    formset = BlogForm(request.POST or None, request.FILES or None, initial=initial)

    if formset.is_valid():
        blog = formset.save()
        messages.success(request, 'Blog draft saved on our database.')
        # FIXME Enable this in the future.
        # new_blog_notification(blog)
        return HttpResponseRedirect(
            reverse('blog_detail', args=[blog.id,])
        )

    # Limit dropdown list to claimant
    if not request.user.is_superuser:
        claimant = Claimant.objects.get(user=request.user)
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
        "title": "Submit blog post draft",
        "formset": formset,
    }
    return render(request, 'lowfat/form.html', context)

@login_required
def blog_detail(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if (request.user.is_superuser or
            Claimant.objects.get(user=request.user) == this_blog.fund.claimant):
        context = {
            'blog': Blog.objects.get(id=blog_id),
            'emails': BlogSentMail.objects.filter(blog=this_blog),
        }

        return render(request, 'lowfat/blog_detail.html', context)

    raise Http404("Blog post does not exist.")

@staff_member_required
def blog_review(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if request.POST:
        # Handle submission
        formset = BlogReviewForm(request.POST, instance=this_blog)

        if formset.is_valid():
            blog = formset.save()
            mail = BlogSentMail(
                **{
                    "justification": formset.cleaned_data['email'],
                    "sender": request.user,
                    "receiver": blog.fund.claimant,
                    "blog": blog,
                }
            )
            mail.save()
            # FIXME Enable this in the future.
            # blog_review_notification(mail)
            return HttpResponseRedirect(
                reverse('blog_detail', args=[blog.id,])
            )

    formset = BlogReviewForm(None, instance=this_blog)

    # Limit dropdown list to staffs
    if not this_blog.reviewer:
        formset.fields["reviewer"].queryset = User.objects.filter(is_staff=True)

    context = {
        'blog': this_blog,
        'emails': BlogSentMail.objects.filter(blog=this_blog),
        'formset': formset,
    }

    return render(request, 'lowfat/blog_review.html', context)

@staff_member_required
def report(request):
    """Report view."""
    # XXX Pandas can't process Django QuerySet so we need to convert it into list.
    # XXX Pandas doesn't support DecimalField so we need to convert it into float.

    # Number of claimants per year
    claimants_per_year = Claimant.objects.all().values('application_year').annotate(total=Count('application_year'))
    claimants_per_year_plot = Bar(
        list(claimants_per_year),
        values='total',
        label='application_year',
        title='Number of claimants'
    )

    # Fund requests
    fund_amount = Fund.objects.all().values('budget_approved')
    fund_amount_hist = Histogram(
        [float(amount['budget_approved']) for amount in list(fund_amount)],
        title='Amount request'
    )

    bokeh_script, bokeh_plots = components(
        {
            'claimants_per_year': claimants_per_year_plot,
            'fund_amount': fund_amount_hist,
        },
        CDN
    )

    context = {
        'bokeh_script': bokeh_script,
    }
    context.update(bokeh_plots)

    return render(request, 'lowfat/report.html', context)

@staff_member_required
def geojson(request):
    """Return the GeoJSON file."""

    context = {
        'claimants': Claimant.objects.all(),
        'funds': Fund.objects.all(),
    }

    return render(request, 'lowfat/map.geojson', context)
