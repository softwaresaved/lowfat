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


class FundForm(ModelForm):
    class Meta:
        model = Fund
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
                'url': "Fund's homepage url",
                'name': "Fund's name",
                }

        widgets = {
            'start_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
            'end_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        }


    required_css_class = 'form-field-required'


class FundReviewForm(ModelForm):
    class Meta:
        model = Fund
        fields = [
                "status",
                #"ad_status",  # TODO uncomment in the future
                "required_blog_posts",
                "budget_approved",
                "notes_from_admin",
                ]


    required_css_class = 'form-field-required'


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = [
            'fund',
            'claim',
            'amount_claimed',
            'recipient',
            'final',
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
                'fund',
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
        fields = [
            'fund',
            'draft_url',
            'final',
                ]


    required_css_class = 'form-field-required'


class BlogReviewForm(ModelForm):
    class Meta:
        model = Blog
        exclude = [
                "fund",
                "added",
                "updated",
                ]


    required_css_class = 'form-field-required'
