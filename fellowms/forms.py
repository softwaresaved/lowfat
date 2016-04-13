from django.forms import ModelForm

from .models import Fellow, Event

class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        fields = '__all__'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
