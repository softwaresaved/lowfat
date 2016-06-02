from django.forms import ModelForm, widgets

from .models import Fellow, Event, Expense, Blog

class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        exclude = [
                "user",
                "home_lon",
                "home_lat",
                "inauguration_year",
                "funding_notes",
                "mentor",
                ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = [
                "status",
                "budget_approve",
                "report_url",
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
        exclude = [
                'status',
                ]
