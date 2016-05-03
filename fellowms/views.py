from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Fellow, Event, Expense, Blog
from .forms import FellowForm, EventForm, ExpenseForm, BlogForm

def index(request):
    context = {
            'fellows': Fellow.objects.all(),
            'events': Event.objects.all(),
            }
    return render(request, 'fellowms/index.html', context)

def dashboard(request):
    return render(request, 'fellowms/dashboard.html')

@login_required
def fellow(request):
    if request.POST:
        # Handle submission
        formset = FellowForm(request.POST, request.FILES)

        if formset.is_valid():
            fellow = formset.save()
            return HttpResponseRedirect(reverse('fellow_detail',
                args=[fellow.id,]))
    else:
        formset = FellowForm

    # Show submission form.
    context = {
            "title": "Create fellow",
            "formset": formset,
            "submit_text": "Save",
            }
    return render(request, 'fellowms/form.html', context)

def fellow_detail(request, fellow_id):
    context = {
            'fellow': Fellow.objects.get(id=fellow_id),
            }

    return render(request, 'fellowms/fellow_detail.html', context)

def event(request):
    if request.POST:
        # Handle submission
        post = request.POST.copy()
        fellow = Fellow.objects.get(email=post['fellow'])
        post['fellow'] = fellow.id
        formset = EventForm(post)

        if formset.is_valid():
            event = formset.save()
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
    context = {
            'event': Event.objects.get(id=event_id),
            }

    return render(request, 'fellowms/event_detail.html', context)

def expense(request):
    if request.POST:
        # Handle submission
        formset = ExpenseForm(request.POST, request.FILES)

        if formset.is_valid():
            expense = formset.save()
            return HttpResponseRedirect(reverse('expense_detail',
                args=[expense.id,]))
    else:
        formset = ExpenseForm

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

def blog(request):
    if request.POST:
        # Handle submission
        formset = BlogForm(request.POST)

        if formset.is_valid():
            blog = formset.save()
            return HttpResponseRedirect(reverse('blog_detail',
                args=[blog.id,]))
    else:
        formset = BlogForm

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
