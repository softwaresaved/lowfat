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
                "application_year",
                "selected",
                "fellowship_grant",
                "mentor",
                "notes_from_admin",
                "added",
                "updated",
                ]


    required_css_class = 'form-field-required'


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = [
                "status",
                "ad_status",
                "budget_approved",
                "notes_from_admin",
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


    required_css_class = 'form-field-required'


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = [
                'id',
                'status',
                'amount_authorized_for_payment',
                "funds_from",
                "notes_from_admin",
                "added",
                "updated",
                ]
        labels = {
                'amount_authorized_for_payment': 'Amount authorized for payment',
                }


    required_css_class = 'form-field-required'


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


    required_css_class = 'form-field-required'


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = [
                'status',
                "notes_from_admin",
                "added",
                "updated",
                ]


    required_css_class = 'form-field-required'
