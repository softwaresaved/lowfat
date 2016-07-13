from django.forms import ModelForm

from .models import *

class FellowForm(ModelForm):
    class Meta:
        model = Fellow
        exclude = [
                "user",
                "home_lon",
                "home_lat",
                "funding_notes",
                "inauguration_year",
                "fellowship_grant",
                "mentor",
                "added",
                "updated",
                ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = [
                "status",
                "ad_status",
                "budget_approve",
                "report_url",
                "added",
                "updated",
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
                "added",
                "updated",
                ]


class ExpenseReviewForm(ModelForm):
    class Meta:
        model = Expense
        exclude = [
                'id',
                'event',
                'proof',
                "added",
                "updated",
                ]


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = [
                'status',
                "added",
                "updated",
                ]
