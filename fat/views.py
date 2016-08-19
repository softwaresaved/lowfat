from datetime import date

import django.utils
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from bokeh.charts import Bar, Histogram
from bokeh.embed import components
from bokeh.resources import CDN

from .models import *
from .forms import *
from .mail import *

def index(request):
    context = {
            'claimeds': Claimed.objects.exclude(selected=False).order_by('application_year').reverse(),
            'funds': Fund.objects.filter(category="H", start_date__gte=django.utils.timezone.now(), can_be_advertise_before=True).order_by("start_date").reverse(),
            }

    if request.user.is_authenticated() and request.user.is_superuser:
        context.update({
            'show_grant_available': True,
            })

    return render(request, 'fat/index.html', context)

@login_required
def dashboard(request):
    context = {}

    if request.user.is_authenticated():
        if not request.user.is_superuser and not request.user.is_staff:
            claimed = Claimed.objects.get(user=request.user)

            context.update({
                'claimed': claimed,
                'funds': Fund.objects.filter(claimed=claimed).reverse(),
                'budget_available': claimed.claimedship_available(),
                })
        else:
            context.update({
                'funds': Fund.objects.filter(status__in=['U', 'P']).reverse(),
                'expenses': Expense.objects.filter(status__in=['W', 'S', 'P']).reverse(),
                'blogs': Blog.objects.filter(status__in=['U', 'R']).reverse(),
                })

    return render(request, 'fat/dashboard.html', context)

@login_required
def claimed(request):
    if not request.user.is_superuser and not request.user.is_staff:
        instance = Claimed.objects.get(user=request.user)
    else:
        instance = None

    formset = ClaimedForm(request.POST or None, request.FILES or None, instance=instance)

    if formset.is_valid():
        claimed = formset.save()
        return HttpResponseRedirect(reverse('claimed_detail',
                                            args=[claimed.id,]))

    # Show submission form.
    context = {
            "title": "Create claimed" if instance is None else "Edit claimed",
            "formset": formset,
            "submit_text": "Save" if instance is None else "Update",
            }
    return render(request, 'fat/form.html', context)

def claimed_detail(request, claimed_id):
    """Details about claimed."""
    this_claimed = Claimed.objects.get(id=claimed_id)

    if not this_claimed.selected:
        raise Http404("Claimed does not exist.")

    context = {
            'claimed': this_claimed,
            'funds': Fund.objects.filter(claimed=this_claimed),
            }

    if request.user.is_authenticated() and (request.user.is_superuser or
            Claimed.objects.get(user=request.user) == this_claimed):
            context.update({
                'expenses': Expense.objects.filter(fund__claimed=this_claimed),
                'show_finances': True,
                })

    return render(request, 'fat/claimed_detail.html', context)

def claimed_slug_resolution(request, claimed_slug):
    """Resolve claimed slug and return the details."""
    try:
        claimed = Claimed.objects.get(slug=claimed_slug, selected=True)
    except:
        claimed = None

    if claimed:
        return claimed_detail(request, claimed.id)

    raise Http404("Claimed does not exist.")

@login_required
def my_profile(request):
    if not request.user.is_superuser and not request.user.is_staff:
        claimed = Claimed.objects.get(user=request.user)
        return claimed_detail(request, claimed.id)

    raise Http404("Claimed does not exist.")

@login_required
def fund(request):
    if request.POST:
        # Handle submission
        post = request.POST.copy()
        claimed = Claimed.objects.get(id=post['claimed'])
        post['claimed'] = claimed.id
        formset = FundForm(post)

        if formset.is_valid():
            fund = formset.save()

            # Default value for budget_approved is budget_total.
            # The reason for this is to save staffs to copy and paste the approved amount.
            fund.budget_approved = fund.budget_total()
            fund.save()

            new_fund_notification(fund)
            return HttpResponseRedirect(reverse('fund_detail',
                args=[fund.id,]))

    if not request.user.is_superuser:
        initial = {
            "claimed": Claimed.objects.get(user=request.user),
        }
    else:
        initial = {}

    formset = FundForm(initial=initial)

    if not request.user.is_superuser:
        formset.fields["claimed"].queryset = Claimed.objects.filter(user=request.user)

    # Show submission form.
    context = {
            "title": "Request fund",
            "formset": formset,
            }
    return render(request, 'fat/form.html', context)

@login_required
def fund_detail(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)
    
    if (request.user.is_superuser or
            Claimed.objects.get(user=request.user) == this_fund.claimed):
        budget_request = this_fund.budget_total()

        context = {
            'fund': this_fund,
            'expenses': Expense.objects.filter(fund=this_fund),
            'blogs': Blog.objects.filter(fund=this_fund),
        }

        return render(request, 'fat/fund_detail.html', context)

    raise Http404("Fund does not exist.")

@staff_member_required
def fund_review(request, fund_id):
    this_fund = Fund.objects.get(id=fund_id)

    if request.POST:
        # Handle submission
        formset = FundReviewForm(request.POST, instance=this_fund)

        if formset.is_valid():
            fund = formset.save()
            mail = FundSentMail(**{
                "justification": formset.cleaned_data['email'],
                "sender": request.user,
                "receiver": fund.claimed,
                "fund": fund,
                })
            mail.save()
            fund_review_notification(mail)
            return HttpResponseRedirect(reverse('fund_detail',
                args=[fund.id,]))

    formset = FundReviewForm(None, instance=this_fund)

    context = {
            'fund': this_fund,
            'formset': formset,
            'emails': FundSentMail.objects.filter(fund=this_fund),
            }

    return render(request, 'fat/fund_review.html', context)

def fund_past(request):
    funds = Fund.objects.filter(
            start_date__lt=django.utils.timezone.now(),
            category="H",
            can_be_advertise_after=True,
            ).order_by("start_date").reverse()

    context = {
            'funds': funds,
            }

    return render(request, 'fat/fund_past.html', context)

@login_required
def expense(request):
    formset = ExpenseForm(request.POST or None, request.FILES or None)

    if formset.is_valid():
        expense = formset.save()
        new_expense_notification(expense)
        return HttpResponseRedirect(reverse('expense_detail',
                                            args=[expense.id,]))

    # Store GET parameters
    fund_id = request.GET.get("fund_id")

    # Setup Fund if provided
    if fund_id:
        initial = {"fund": Fund.objects.get(id=fund_id)}
    else:
        initial = {}

    formset = ExpenseForm(initial=initial)

    # Limit dropdown list to claimed
    if not request.user.is_superuser:
        claimed = Claimed.objects.get(user=request.user)
        formset.fields["fund"].queryset = Fund.objects.filter(claimed=claimed)

    # Show submission form.
    context = {
            "title": "Submit expense claim",
            "formset": formset,
            }
    return render(request, 'fat/form.html', context)

@login_required
def expense_detail(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)
    
    if (request.user.is_superuser or
            Claimed.objects.get(user=request.user) == this_expense.fund.claimed):
        context = {
            'expense': Expense.objects.get(id=expense_id),
        }

        return render(request, 'fat/expense_detail.html', context)

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
            mail = ExpenseSentMail(**{
                "justification": formset.cleaned_data['email'],
                "sender": request.user,
                "receiver": expense.fund.claimed,
                "expense": expense,
                })
            mail.save()
            expense_review_notification(mail)
            return HttpResponseRedirect(reverse('expense_detail',
                args=[expense.id,]))

    formset = ExpenseReviewForm(None, instance=this_expense)

    context = {
            'expense': this_expense,
            'formset': formset,
            'emails': ExpenseSentMail.objects.filter(expense=this_expense),
            }

    return render(request, 'fat/expense_review.html', context)

@staff_member_required
def expense_review_relative(request, fund_id, expense_relative_number):
    this_fund = Fund.objects.get(id=fund_id)
    this_expense = Expense.objects.get(fund=this_fund, relative_number=expense_relative_number)
    return expense_review(request, this_expense.id)

@login_required
def blog(request):
    formset = BlogForm(request.POST or None, user=request.user)

    if formset.is_valid():
        blog = formset.save()
        new_blog_notification(blog)
        return HttpResponseRedirect(reverse('blog_detail',
                                            args=[blog.id,]))

    fund_id = request.GET.get("fund_id")
    if fund_id:
        initial = {"fund": Fund.objects.get(id=fund_id)}
    else:
        initial = {}
        formset = BlogForm(initial=initial)

        # Limit dropdown list to claimed
    if not request.user.is_superuser:
        claimed = Claimed.objects.get(user=request.user)
        formset.fields["fund"].queryset = Fund.objects.filter(claimed=claimed)

    # Show submission form.
    context = {
            "title": "Submit blog",
            "formset": formset,
            }
    return render(request, 'fat/form.html', context)

@login_required
def blog_detail(request, blog_id):
    context = {
            'blog': Blog.objects.get(id=blog_id),
            }

    return render(request, 'fat/blog_detail.html', context)

@staff_member_required
def blog_review(request, blog_id):
    this_blog = Blog.objects.get(id=blog_id)

    if request.POST:
        # Handle submission
        formset = BlogReviewForm(request.POST, instance=this_blog)

        if formset.is_valid():
            blog = formset.save()
            mail = BlogSentMail(**{
                "justification": formset.cleaned_data['email'],
                "sender": request.user,
                "receiver": blog.fund.claimed,
                "blog": blog,
                })
            mail.save()
            blog_review_notification(mail)
            return HttpResponseRedirect(reverse('blog_detail',
                args=[blog.id,]))

    formset = BlogReviewForm(None, instance=this_blog)

    # Limit dropdown list to staffs
    if not this_blog.reviewer:
        formset.fields["reviewer"].queryset = User.objects.filter(is_staff=True)

    context = {
            'blog': this_blog,
            'emails': BlogSentMail.objects.filter(blog=this_blog),
            'formset': formset,
            }

    return render(request, 'fat/blog_review.html', context)

@staff_member_required
def report(request):
    """Report view."""
    # XXX Pandas can't process Django QuerySet so we need to convert it into list.
    # XXX Pandas doesn't support DecimalField so we need to convert it into float.

    # Number of claimeds per year
    claimeds_per_year = Claimed.objects.all().values('application_year').annotate(total=Count('application_year'))
    claimeds_per_year_plot = Bar(list(claimeds_per_year),
               values='total',
               label='application_year',
               title='Number of claimeds')

    # Fund requests
    fund_amount = Fund.objects.all().values('budget_approved')
    fund_amount_hist = Histogram([float(amount['budget_approved']) for amount in list(fund_amount)],
                                  title='Amount request')

    bokeh_script, bokeh_plots = components({
        'claimeds_per_year': claimeds_per_year_plot,
        'fund_amount': fund_amount_hist,
        }, CDN)

    context = {
        'bokeh_script': bokeh_script,
        }
    context.update(bokeh_plots)

    return render(request, 'fat/report.html', context)

@staff_member_required
def geojson(request):
    """Return the GeoJSON file."""

    context = {
            'claimeds': Claimed.objects.all(),
            'funds': Fund.objects.all(),
            }

    return render(request, 'fat/map.geojson', context)
