from django.shortcuts import render

from .models import Fellow, Event
from .forms import FellowForm, EventForm

def fellow(request):
    if request.POST:
        # Handle submission
        new_fellow = FellowForm(request.POST)

        new_fellow.save()

    # Show submission form.
    context = {
            "formset": FellowForm,
            }
    return render(request, 'fellowms/fellow.html', context)

def event(request):
    if request.POST:
        # Handle submission
        new_event = EventForm(request.POST)

        new_event.save()

    # Show submission form.
    context = {
            "formset": EventForm,
            }
    return render(request, 'fellowms/event.html', context)


def board(request):
    context = {
            'fellows': Fellow.objects.all(),
            'events': Event.objects.all(),
            }
    return render(request, 'fellowms/board.html', context)
