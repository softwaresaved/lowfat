from django.forms import ModelForm, SelectDateWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import PrependedText

from .models import *

class FellowForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FellowForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<h2>Personal details</h2>'),
                'forenames',
                'surname',
                'email',
                'phone',
                'gender',
                'home_country',
                'home_city',
                'photo',
                HTML('<h2>Professional details</h2>'),
                'research_area',
                'research_area_code',
                'affiliation',
                'funding',
                'funding_notes',
                'work_description',
                HTML('<h2>Social Networks</h2>'),
                'website',
                'website_feed',
                'orcid',
                'github',
                'gitlab',
                'twitter',
                'facebook',
                ButtonHolder(
                    Submit('submit', 'Add')
                )
            )
            )

    class Meta:
        model = Fellow
        fields = [
            'forenames',
            'surname',
            'email',
            'phone',
            'gender',
            'home_country',
            'home_city',
            'photo',
            'research_area',
            'research_area_code',
            'affiliation',
            'funding',
            'funding_notes',
            'work_description',
            'website',
            'website_feed',
            'orcid',
            'github',
            'gitlab',
            'twitter',
            'facebook',
            ]


    required_css_class = 'form-field-required'


class FundForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FundForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<p>To apply for expenses for eligible events, please fill in this form at least one month before the start date of the event you wish to attend or organise.</p><h2>Fellow details</h2>'),
                'fellow',
                HTML('<h2>Event details</h2>'),
                'category',
                'name',
                'url',
                'country',
                'city',
                'start_date',
                'end_date',
                HTML('<h2>Costs</h2><p>Please provide an estimate of your costs below. All values should be entered in GBP. Note that the cost entered here must be within 20% of the expenses you submit. See the terms and conditions for details (http://www.software.ac.uk/fellowship-terms-and-conditions-2016)</p><p>Please fill in all cost sections that are relevant to your event type.</p><p>Total costs should reflect the sum of all the costs and be the total estimate of costs for this event.</p>'),
                PrependedText('budget_request_travel', '£'),
                PrependedText('budget_request_attendance_fees', '£'),
                PrependedText('budget_request_subsistence_cost', '£'),
                PrependedText('budget_request_venue_hire', '£'),
                PrependedText('budget_request_catering', '£'),
                PrependedText('budget_request_others', '£'),
                HTML('<h2>Justification for attending or organising the event</h2><p>When filling in the questions below please consider the following points:<p></p>For attending conferences/workshops: will the conference focus on a significant field, will you meet significant researchers, will there be a focus on research software?</p><p>For organising workshops: how will the event help your domain, how will the event help the Institute, how will the event help you.</p><p>For policy related work: how might participation or organisation help the policy goals of the Institute, such as improving software and improved research (this can include people and tools perspectives).</p><p>For other: please state reasons - note it maybe good to discuss matter with the Institute Community Lead before filling the form to make sure the rationale is aligned to the Institute and to your own objectives.</p>'),
                'justification',
                'additional_info',
                HTML('<h2>Sponsored</h2><p>Please list who is going to be sponsored.</p>'),
                'extra_sponsored',
                HTML('<h2>Permissions</h2>'),
                'can_be_advertise_before',
                'can_be_advertise_after',
                ButtonHolder(
                    Submit('submit', 'Add')
                )
            )
            )

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
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                'claim',
                PrependedText('amount_claimed', '£'),
                'recipient',
                'final',
                )
            )

    class Meta:
        model = Expense
        fields = [
            'fund',
            'claim',
            'amount_claimed',
            'recipient',
            'final',
                ]


    required_css_class = 'form-field-required'


class ExpenseReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpenseReviewForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                'status',
                'received_date',
                'asked_for_authorization_date',
                'send_to_finance_date',
                PrependedText('amount_authorized_for_payment', '£'),
                'funds_from',
                'grant_used',
                'notes_from_admin',
                )
            )

    class Meta:
        model = Expense
        fields = [
            'status',
            'received_date',
            'asked_for_authorization_date',
            'send_to_finance_date',
            'amount_authorized_for_payment',
            'funds_from',
            'grant_used',
            'notes_from_admin',
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
