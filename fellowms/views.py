from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bokeh.charts import Bar, Histogram
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN

from .models import *
from .forms import *
from .mail import *

def index(request):
    context = {
            'fellows': Fellow.objects.exclude(inauguration_year=None).order_by('inauguration_year').reverse(),
            'events': Event.objects.filter(category="H").order_by("start_date").reverse(),
            }
    return render(request, 'fellowms/index.html', context)

def dashboard(request):
    context = {}

    if request.user.is_authenticated():
        if not request.user.is_superuser and not request.user.is_staff:
            fellow = Fellow.objects.get(user=request.user)

            context.update({
                'fellow': fellow,
                'events': Event.objects.filter(fellow=fellow),
                'budget_available': fellow.fellowship_available(),
                })
        else:
            context.update({
                'events': Event.objects.filter(status__in=['U', 'P']),
                'expenses': Expense.objects.filter(status__in=['W', 'S', 'P']),
                'blogs': Blog.objects.filter(status__in=['U', 'R']),
                })

    return render(request, 'fellowms/dashboard.html', context)

@login_required
def fellow(request):
    if not request.user.is_superuser and not request.user.is_staff:
       instance = Fellow.objects.get(user=request.user)
    else:
       instance = None

    if request.POST:
        # Handle submission
        formset = FellowForm(request.POST, request.FILES, instance=instance)

        if formset.is_valid():
            fellow = formset.save()
            return HttpResponseRedirect(reverse('fellow_detail',
                args=[fellow.id,]))
    else:
        formset = FellowForm(None, instance=instance)

    # Show submission form.
    context = {
            "title": "Create fellow",
            "formset": formset,
            "submit_text": "Save",
            }
    return render(request, 'fellowms/form.html', context)

def fellow_detail(request, fellow_id):
    this_fellow = Fellow.objects.get(id=fellow_id)
    context = {
            'fellow': this_fellow,
            'events': Event.objects.filter(fellow=this_fellow),
            }

    if request.user.is_authenticated() and (request.user.is_superuser or
            Fellow.objects.get(user=request.user) == this_fellow):
            context.update({
                'show_finances': True,
                })

    return render(request, 'fellowms/fellow_detail.html', context)

def event(request):
    if request.POST:
        # Handle submission
        post = request.POST.copy()
        fellow = Fellow.objects.get(id=post['fellow'])
        post['fellow'] = fellow.id
        formset = EventForm(post)

        if formset.is_valid():
            event = formset.save()
            new_event_notification(event)
            return HttpResponseRedirect(reverse('event_detail',
                args=[event.id,]))
    else:
        formset = EventForm

    # Show submission form.
    context = {
            "title": "Submit event",
            "formset": formset,
            "submit_text": "Submit",
            }
    return render(request, 'fellowms/form.html', context)

def event_detail(request, event_id):
    this_event = Event.objects.get(id=event_id)
    
    context = {
            'event': this_event,
                }

    if request.user.is_authenticated():
        if (request.user.is_superuser or
            Fellow.objects.get(user=request.user) == this_event.fellow):
            budget_request = this_event.budget_total()

            context.update({
                    'expenses': Expense.objects.filter(event=this_event),
                    'blogs': Blog.objects.filter(event=this_event),
                    'budget_request': budget_request,
                    })

    return render(request, 'fellowms/event_detail.html', context)

def event_past(request):
    events = Event.objects.filter(
            start_date__lt=date.today(),
            category="H"
            ).order_by("start_date").reverse()

    context = {
            'events': events,
            }

    return render(request, 'fellowms/event_past.html', context)

def expense(request):
    if request.POST:
        # Handle submission
        formset = ExpenseForm(request.POST, request.FILES)

        if formset.is_valid():
            expense = formset.save()
            new_expense_notification(expense)
            return HttpResponseRedirect(reverse('expense_detail',
                args=[expense.id,]))
    else:
        event_id = request.GET.get("event_id")
        if event_id:
            initial = {"event": Event.objects.get(id=event_id)}
        else:
            initial = {}
        formset = ExpenseForm(initial=initial)

    # Show submission form.
    context = {
            "title": "Submit expenses",
            "formset": formset,
            "submit_text": "Submit",
            }
    return render(request, 'fellowms/form.html', context)

def expense_detail(request, expense_id):
    context = {
            'expense': Expense.objects.get(id=expense_id),
            }

    return render(request, 'fellowms/expense_detail.html', context)

def expense_review(request, expense_id):
    this_expense = Expense.objects.get(id=expense_id)

    if request.POST:
        # Handle submission
        formset = ExpenseReviewForm(request.POST, instance=this_expense)

        if formset.is_valid():
            expense = formset.save()
            return HttpResponseRedirect(reverse('expense_detail',
                args=[expense.id,]))

    formset = ExpenseReviewForm(None, instance=this_expense)

    context = {
            'expense': this_expense,
            'formset': formset,
            'submit_text': 'Update',
            }

    return render(request, 'fellowms/expense_review.html', context)

def blog(request):
    if request.POST:
        # Handle submission
        formset = BlogForm(request.POST)

        if formset.is_valid():
            blog = formset.save()
            new_blog_notification(blog)
            return HttpResponseRedirect(reverse('blog_detail',
                args=[blog.id,]))
    else:
        event_id = request.GET.get("event_id")
        if event_id:
            initial = {"event": Event.objects.get(id=event_id)}
        else:
            initial = {}
        formset = BlogForm(initial=initial)

    # Show submission form.
    context = {
            "title": "Submit blog",
            "formset": formset,
            "submit_text": "Submit",
            }
    return render(request, 'fellowms/form.html', context)

def blog_detail(request, blog_id):
    context = {
            'blog': Blog.objects.get(id=blog_id),
            }

    return render(request, 'fellowms/blog_detail.html', context)

@staff_member_required
def report(request):
    """Report view."""
    # XXX Pandas can't process Django QuerySet so we need to convert it into list.
    # XXX Pandas doesn't support DecimalField so we need to convert it into float.

    # Number of fellows per year
    fellows_per_year = Fellow.objects.all().values('inauguration_year').annotate(total=Count('inauguration_year'))
    fellows_per_year_plot = Bar(list(fellows_per_year),
               values='total',
               label='inauguration_year',
               title='Number of fellows')

    # Event requests
    event_amount = Event.objects.all().values('budget_approve')
    event_amount_hist = Histogram([float(amount['budget_approve']) for amount in list(event_amount)],
                                  title='Amount request')

    bokeh_script, bokeh_plots = components({
        'fellows_per_year': fellows_per_year_plot,
        'event_amount': event_amount_hist,
        }, CDN)

    context = {
        'bokeh_script': bokeh_script,
        }
    context.update(bokeh_plots)

    return render(request, 'fellowms/report.html', context)

def geojson(request):
    """Return the GeoJSON file."""

    context = {
            'fellows': Fellow.objects.all(),
            'events': Event.objects.all(),
            }

    return render(request, 'fellowms/map.geojson', context)
