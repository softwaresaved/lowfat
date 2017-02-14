from datetime import datetime

from django.forms import Form, ModelForm, SelectDateWidget, CharField, Textarea, FileField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import PrependedText

from .models import *

TODAY_YEAR = datetime.now().year
SELECT_DATE_WIDGE_YEARS = [TODAY_YEAR + delta for delta in range(-3, 4)]

class GarlicForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GarlicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {
            'data_persist': "garlic",
        }


class ClaimantForm(GarlicForm):
    class Meta:
        model = Claimant
        fields = [
            'forenames',
            'surname',
            'email',
            'phone',
            'gender',
            'home_country',
            'home_city',
            'affiliation',
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

    def __init__(self, *args, **kwargs):
        super(ClaimantForm, self).__init__(*args, **kwargs)

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
                HTML('<h2>Professional details</h2>'),
                'affiliation',
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


class FellowForm(GarlicForm):
    class Meta:
        model = Claimant
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

    def __init__(self, *args, **kwargs):
        super(FellowForm, self).__init__(*args, **kwargs)

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


class FundForm(GarlicForm):
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

        labels = {
            'claimant': 'Requester name',
            'category_other': 'Specify the category if used "Other"',
            'name': 'Event name',
            'url': 'Event webpage link',
            'country': 'Country in which event is taking place',
            'city': 'City in which the event is taking place',
            'start_date': 'Start date of event',
            'end_date': 'End date of event',
            'budget_request_travel': "Travel costs",
            'budget_request_attendance_fees': "Attendance fees (e.g. workshop / event registration costs)",
            'budget_request_subsistence_cost': "Subsistence costs (e.g. accommodation and meals)",
            'budget_request_venue_hire': "Venue hire",
            'budget_request_catering': "Catering",
            'budget_request_others': "Other costs",
            'can_be_advertise_before': "Can we promote your involvement in this event before it takes place?",
            'can_be_advertise_after': "Can we promote your involvement in this event after it takes place?"
        }

        widgets = {
            'start_date': SelectDateWidget(
                years=SELECT_DATE_WIDGE_YEARS,
                empty_label=("Choose Year", "Choose Month", "Choose Day")
            ),
            'end_date': SelectDateWidget(
                years=SELECT_DATE_WIDGE_YEARS,
                empty_label=("Choose Year", "Choose Month", "Choose Day")
            ),
        }


    required_css_class = 'form-field-required'
    total_budget = CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(FundForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<p>To apply for expenses for eligible events, please fill in this form at least one month before the start date of the event you wish to attend or organise.</p><h2>Requester details</h2>'),
                'claimant',
                HTML('<h2>Funding request details</h2>'),
                'category',
                'category_other',
                'name',
                'url',
                'country',
                'city',
                'start_date',
                'end_date',
                HTML('<h2>Costs</h2><p>Please provide an estimate of your costs below. All values should be entered in GBP. Note that the cost entered here must be within 20% of the expenses you submit. See the terms and conditions for details (<a href="http://www.software.ac.uk/fellowship-terms-and-conditions-{% now "Y" %}">http://www.software.ac.uk/fellowship-terms-and-conditions-{% now "Y" %}</a>)</p><p>Please fill in all cost sections that are relevant to your event type.</p>'),
                PrependedText('budget_request_travel', '£', onkeyup="update_budget()"),
                PrependedText('budget_request_attendance_fees', '£', onkeyup="update_budget()"),
                PrependedText('budget_request_subsistence_cost', '£', onkeyup="update_budget()"),
                PrependedText('budget_request_venue_hire', '£', onkeyup="update_budget()"),
                PrependedText('budget_request_catering', '£', onkeyup="update_budget()"),
                PrependedText('budget_request_others', '£', onkeyup="update_budget()"),
                PrependedText('total_budget', '£', disabled=True, value=0.0),
                HTML('<h2>Justification for attending or organising the event</h2><p>When filling in the questions below please consider the following points:</p><ul><li>For attending conferences/workshops: will the conference focus on a significant field, will you meet significant researchers, will there be a focus on research software?</li><li>For organising workshops: how will the event help your domain, how will the event help the Institute, how will the event help you.</li><li>For policy related work: how might participation or organisation help the policy goals of the Institute, such as improving software and improved research (this can include people and tools perspectives).</li><li>For other: please state reasons - note it maybe good to discuss matter with the Institute Community Lead before filling the form to make sure the rationale is aligned to the Institute and to your own objectives.</li></ul>'),
                'justification',
                'additional_info',
                HTML('<h2>Sponsorship</h2><p>If you are sponsoring others to take part in this event from your Fellowship funds please give their names and email addresses below, if you do not know their names at this stage please state whether there is sponsorship of others needed in this request. In either case please provide some justification.</p>'),
                'extra_sponsored',
                HTML('<h2>Publicity</h2>'),
                'can_be_advertise_before',
                'can_be_advertise_after',
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
            )

        # Force user to select one category
        self.fields['category'].widget.choices.insert(0, ('', '---------'))
        self.fields['category'].initial = ''


class FundReviewForm(GarlicForm):
    class Meta:
        model = Fund
        fields = [
            "status",
            #"ad_status",  # TODO uncomment in the future
            "required_blog_posts",
            "budget_approved",
            "notes_from_admin",
        ]

        labels = {
            'budget_approved': 'Total budget approved',
        }


    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(FundReviewForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Submit'))


class FundImportForm(Form):
    required_css_class = 'form-field-required'
    csv = FileField()

    def __init__(self, *args, **kwargs):
        super(FundImportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {
            'data_persist': "garlic",
        }

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML("""Your CSV <strong>must</strong> have the following columns:
<ul>
<li>Forename(s)</li>
<li>Surname</li>
<li>Event type</li>
<li>Event name</li>
<li>Event website</li>
<li>Event Country</li>
<li>Event City</li>
<li>Start date</li>
<li>End date</li>
<li>Travel costs</li>
<li>Conference/Workshop attendance fees</li>
<li>Subsistence costs</li>
<li>Venue hire</li>
<li>Catering</li>
<li>Travel and subsistence cost for those being paid to attend your organised event</li>
<li>Other costs</li>
<li>How is the event relevant to the work of the Software Sustainability Institute?</li>
<li>Any other information relevant to this application?</li>
<li>Estimate</li>
<li>Submitted</li>
<li>Revised estimate</li>
<li>Approved</li>
</ul>
<p class="text-danger">You will not have access to debug information!</p>"""),
                'csv',
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
            )


class ExpenseForm(GarlicForm):
    class Meta:
        model = Expense
        fields = [
            'fund',
            'claim',
            'amount_claimed',
            'justification_for_extra',
            'final',
            'recipient_fullname',
            'recipient_email',
            'recipient_affiliation',
            'recipient_group',
            'recipient_connection',
        ]

        labels = {
            'fund': 'Open approved funding request',
            'claim': 'PDF copy of claim and receipt(s)',
            'justification_for_extra': "If the claim is greater than 20% of the amount requested please provide justification",
            'final': "Is this the final expense claim associated with this funding request?",
            'recipient_fullname': "Full name",
            'recipient_email': "E-mail",
            'recipient_affiliation': "Affiliation",
            'recipient_group': "Group",
            'recipient_connection': "Reason for claim on their behalf",
        }


    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML("</p><a href='https://www.software.ac.uk/fellowship-terms-and-conditions-{% now 'Y' %}'>Terms and conditions apply.</a></p>"),
                'fund',
                HTML("</p>If your funding request isn't on the drop down menu above please email <a href='mailto:{{ settings.FELLOWS_MANAGEMENT_EMAIL }}'>us</a>."),
                'claim',
                HTML("</p>Please follow the guidelines at <a href='https://www.software.ac.uk/fellowship-terms-and-conditions-{% now 'Y' %}'#how-to-apply-for-and-claim-expenses>Fellowship Programme's terms and conditions.</a></p>"),
                PrependedText('amount_claimed', '£'),
                HTML("{% if fund %}<p class='text-warning'>Note that you only have <strong>£{{ fund.expenses_claimed_left }}</strong> left.</p>{% endif %}"),
                'justification_for_extra',
                'final',
                HTML("<h2>Recipient</h2><p>Only fill this part if you are claiming this expense on behalf of someone.</p>"),
                'recipient_fullname',
                'recipient_email',
                'recipient_affiliation',
                'recipient_group',
                'recipient_connection',
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
                )
            )

        self.fields['fund'].queryset = Fund.objects.filter(status__in=['A'])

class ExpenseReviewForm(GarlicForm):
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
            'received_date': SelectDateWidget(
                years=SELECT_DATE_WIDGE_YEARS,
                empty_label=("Choose Year", "Choose Month", "Choose Day")
            ),
            'asked_for_authorization_date': SelectDateWidget(
                years=SELECT_DATE_WIDGE_YEARS,
                empty_label=("Choose Year", "Choose Month", "Choose Day")
            ),
            'send_to_finance_date': SelectDateWidget(
                years=SELECT_DATE_WIDGE_YEARS,
                empty_label=("Choose Year", "Choose Month", "Choose Day")
            ),
        }


    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(ExpenseReviewForm, self).__init__(*args, **kwargs)

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
                'email',
                ButtonHolder(
                    Submit('submit', 'Update')
                )
                )
            )


class BlogForm(GarlicForm):
    class Meta:
        model = Blog
        fields = [
            'fund',
            'draft_url',
            'final',
        ]
        labels = {
            'fund': 'Open approved funding request',
            'draft_url': 'URL of blog post draft',
            'final': "Is this the final blog post you would like to associate with this funding request?",
            }


    required_css_class = 'form-field-required'

    def __init__(self, *args, user=None, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                'draft_url',
                'final',
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
                )
            )

        if user:
            self.fields['fund'].queryset = Fund.objects.filter(status__in=['A'])


class BlogReviewForm(GarlicForm):
    class Meta:
        model = Blog
        exclude = [
            "fund",
            "added",
            "updated",
        ]


    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(BlogReviewForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Update'))
