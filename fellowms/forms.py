from django.forms import ModelForm, widgets

from .models import Fellow, Event, Expense, Blog

class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        fields = '__all__'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        # We don't want to expose fellows' data
        # so we will request the email
        # and match on the database.
        widgets = {
                'fellow': widgets.TextInput(),
                }
        lables = {
                'fellow': 'Email',
                }


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = ['status']


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
