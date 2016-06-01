from django.forms import ModelForm, widgets

from .models import Fellow, Event, Expense, Blog

class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        exclude = [
                "home_lon",
                "home_lat",
                "inauguration_year",
                "mentor",
                ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = [
                "status",
                "budget_approve",
                ]

        # We don't want to expose fellows' data
        # so we will request the email
        # and match on the database.
        labels = {
                'fellow': 'Fellow',
                'url': "Event's homepage url",
                'name': "Event's name",
                }


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = [
                'id',
                'status',
                ]


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
