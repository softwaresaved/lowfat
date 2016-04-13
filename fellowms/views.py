from django.shortcuts import render

from .models import Fellow, Event
from .forms import FellowForm, EventForm

def fellow(request):
    if request.POST:
        # Handle submission
        formset = FellowForm(request.POST)

        if formset.is_valid():
            formset.save()
    else:
        formset = FellowForm

    # Show submission form.
    context = {
            "formset": formset,
            }
    return render(request, 'fellowms/fellow.html', context)

def event(request):
    if request.POST:
        # Handle submission
        formset = EventForm(request.POST)

        if formset.is_valid():
            formset.save()
    else:
        formset = EventForm

    # Show submission form.
    context = {
            "formset": formset,
            }
    return render(request, 'fellowms/event.html', context)


def board(request):
    context = {
            'fellows': Fellow.objects.all(),
            'events': Event.objects.all(),
            }
    return render(request, 'fellowms/board.html', context)
