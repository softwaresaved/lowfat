from django.forms import ModelForm, widgets

from .models import Collaborator, Fellow, Event, Expense, Blog

class CollaboratorForm(ModelForm):
    class Meta:
        model = Collaborator
        exclude = [
                "user",
                "home_lon",
                "home_lat",
                ]


class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        exclude = [
                "funding_notes",
                "inauguration_year",
                "fellowship_grant",
                "mentor",
                ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = [
                "status",
                "ad_status",
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
