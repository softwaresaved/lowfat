from django.forms import ModelForm, SelectDateWidget

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
                "required_blog_posts",
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

        widgets = {
            'start_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
            'end_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        }


    required_css_class = 'form-field-required'


class EventReviewForm(ModelForm):
    class Meta:
        model = Event
        fields = [
                "status",
                "ad_status",
                "required_blog_posts",
                "budget_approved",
                "notes_from_admin",
                ]


    required_css_class = 'form-field-required'


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        exclude = [
                'id',
                'status',
                'received_date',
                'asked_for_authorization_date',
                'send_to_finance_date',
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
                'claim',
                "added",
                'received_date',
                "updated",
                ]

        widgets = {
            'received_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
            'asked_for_authorization_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
            'send_to_finance_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        }


    required_css_class = 'form-field-required'


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = [
                'status',
                "notes_from_admin",
                'published_url',
                "added",
                "updated",
                ]


    required_css_class = 'form-field-required'


class BlogReviewForm(ModelForm):
    class Meta:
        model = Blog
        exclude = [
                "event",
                "added",
                "updated",
                ]


    required_css_class = 'form-field-required'
