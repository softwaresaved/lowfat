from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Fellow, Event, Expense
from .forms import FellowForm, EventForm, ExpenseForm

def fellow(request):
    if request.POST:
        # Handle submission
        formset = FellowForm(request.POST)

        if formset.is_valid():
            fellow = formset.save()
            return HttpResponseRedirect(reverse('fellow_detail',
                args=[fellow.id,]))
    else:
        formset = FellowForm

    # Show submission form.
    context = {
            "formset": formset,
            }
    return render(request, 'fellowms/fellow.html', context)

def fellow_detail(request, fellow_id):
    context = {
            'fellow': Fellow.objects.get(id=fellow_id),
            }

    return render(request, 'fellowms/fellow_detail.html', context)

def event(request):
    if request.POST:
        # Handle submission
        post = request.POST.copy()
        print(post)
        fellow = Fellow.objects.get(email=post['fellow'])
        print(fellow)
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
            "formset": formset,
            }
    return render(request, 'fellowms/event.html', context)

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
            "formset": formset,
            }
    return render(request, 'fellowms/expense.html', context)

def expense_detail(request, expense_id):
    context = {
            'expense': Expense.objects.get(id=expense_id),
            }

    return render(request, 'fellowms/expense_detail.html', context)


def board(request):
    context = {
            'fellows': Fellow.objects.all(),
            'events': Event.objects.all(),
            }
    return render(request, 'fellowms/board.html', context)
