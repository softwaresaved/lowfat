from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime
import logging
import sys
import textwrap

from django.contrib.auth import get_user_model
from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    ChoiceField,
    EmailField,
    FileField,
    Form,
    ModelForm,
    Select,
    SelectMultiple,
    Textarea,
    ValidationError,
)

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML

from . import models

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

TODAY_YEAR = datetime.now().year
SELECT_DATE_WIDGE_YEARS = [TODAY_YEAR + delta for delta in range(-3, 4)]


class GarlicForm(ModelForm):
    not_send_email_field = BooleanField(
        widget=CheckboxInput,
        required=False,
        initial=False,
        label="Suppress email notification for this update to claimant?"
    )
    not_copy_email_field = BooleanField(
        widget=CheckboxInput,
        required=False,
        initial=True,
        label="Suppress copy of email to staff?"
    )

    def __init__(self, *args, **kwargs):
        # Add staff option to not send email notification
        self.is_staff = kwargs.pop("is_staff", False)

        # Set up Garlic attribute to persistent data
        super(GarlicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {
            'data_persist': "garlic",
        }


class ClaimantForm(GarlicForm):
    class Meta:
        model = models.Claimant
        fields = [
            'forenames',
            'surname',
            'email',
            'phone',
            'gender',
            'home_country',
            'home_city',
            'career_stage_when_apply',
            'career_stage_other',
            'affiliation',
            'work_description',
            'institutional_website',
            'website',
            'website_feed',
            'orcid',
            'google_scholar',
            'github',
            'gitlab',
            'bitbucket',
            'twitter',
            'linkedin',
            'facebook',
        ]

    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'career_stage_when_apply',
                'career_stage_other',
                'affiliation',
                'work_description',
                HTML('<h2>Social Networks</h2>'),
                'institutional_website',
                'website',
                'website_feed',
                PrependedText(
                    'orcid',
                    'https://orcid.org/'
                ),
                PrependedText(
                    'google_scholar',
                    'https://scholar.google.co.uk/citations?user='
                ),
                PrependedText(
                    'github',
                    'https://gihub.com/'
                ),
                PrependedText(
                    'gitlab',
                    'https://gitlab.com/'
                ),
                PrependedText(
                    'bitbucket',
                    'https://bitbucket.org/'
                ),
                PrependedText(
                    'linkedin',
                    'https://www.linkedin.com/in/'
                ),
                PrependedText(
                    'twitter',
                    'https://twitter.com/'
                ),
                PrependedText(
                    'facebook',
                    'https://facebook.com/'
                ),
                ButtonHolder(
                    Submit('submit', 'Add')
                )
            )
        )
        self.fields['career_stage_other'].label = "If Other, please describe your career stage"
        self.fields['career_stage_other'].help_text = "Only fill this in if you selected 'My career stage is not reflected in these options.'"

    def clean(self):
        cleaned_data = super().clean()
        career_stage = cleaned_data.get('career_stage_when_apply')
        other = cleaned_data.get('career_stage_other')

        if career_stage == '5' and not other:
            self.add_error('career_stage_other', 'Please describe your career stage.')

        if career_stage != '5' and other:
            self.add_error('career_stage_other', "Please leave this blank unless you selected 'Other'.")

        return cleaned_data





class FellowForm(GarlicForm):
    class Meta:
        model = models.Claimant
        fields = [
            'forenames',
            'surname',
            'email',
            'phone',
            'gender',
            'home_country',
            'home_city',
            'photo',
            'photo_work_description',
            'career_stage_when_apply',
            'career_stage_other',
            'job_title_when_apply',
            'research_area',
            'research_area_code',
            'affiliation',
            'department',
            'group',
            'funding',
            'funding_notes',
            'interests',
            'work_description',
            'institutional_website',
            'website',
            'website_feed',
            'orcid',
            'google_scholar',
            'github',
            'gitlab',
            'bitbucket',
            'twitter',
            'linkedin',
            'facebook',
        ]

        labels = {
            'home_country': "Country",
            'home_city': "City",
            'photo': "Photo (Thumbnail)",
            'photo_work_description': "Photo (Main)",
            'career_stage_when_apply': "Career Stage",
            'job_title_when_apply': "Job Title",
            'research_area_code': "Research Classification",
            'affiliation': "Home institution",
            'department': "Department",
            'group': "Group within Department",
            'funding': "Primary funding body/charity/organisation",
            'funding_notes': "Any additional funders",
            'work_description': "Short Biography",
        }

    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'photo_work_description',
                'photo',
                HTML('<h2>Professional details</h2>'),
                'career_stage_when_apply',
                'career_stage_other',
                'job_title_when_apply',
                'research_area',
                'research_area_code',
                'affiliation',
                'department',
                'group',
                'funding',
                'funding_notes',
                HTML('<h2>Information for the website</h2>'),
                'interests',
                'work_description',
                HTML('<h2>Social Networks</h2>'),
                'institutional_website',
                'website',
                'website_feed',
                PrependedText(
                    'orcid',
                    'https://orcid.org/'
                ),
                PrependedText(
                    'google_scholar',
                    'https://scholar.google.co.uk/citations?user='
                ),
                PrependedText(
                    'github',
                    'https://gihub.com/'
                ),
                PrependedText(
                    'gitlab',
                    'https://gitlab.com/'
                ),
                PrependedText(
                    'bitbucket',
                    'https://bitbucket.org/'
                ),
                PrependedText(
                    'linkedin',
                    'https://www.linkedin.com/in/'
                ),
                PrependedText(
                    'twitter',
                    'https://twitter.com/'
                ),
                PrependedText(
                    'facebook',
                    'https://facebook.com/'
                ),
                ButtonHolder(
                    Submit('submit', 'Add')
                )
            )
        )
        self.fields['career_stage_other'].label = "If Other, please describe your career stage"
        self.fields['career_stage_other'].help_text = "Only fill this in if you selected 'My career stage is not reflected in these options.'"

    def clean(self):
        cleaned_data = super().clean()
        career_stage = cleaned_data.get('career_stage_when_apply')
        other = cleaned_data.get('career_stage_other')

        if career_stage == '5' and not other:
            self.add_error('career_stage_other', 'Please describe your career stage.')

        if career_stage != '5' and other:
            self.add_error('career_stage_other', "Please leave this blank unless you selected 'Other'.")


        return cleaned_data

class FundForm(GarlicForm):
    class Meta:
        model = models.Fund
        exclude = [  # pylint: disable=modelform-uses-exclude
            "success_reported",
            "status",
            "ad_status",
            "budget_approved",
            "required_blog_posts",
            "grant_heading",
            "grant",
            "notes_from_admin",
            "added",
            "approved",
            "updated",
            "approval_chain",
        ]

        labels = {
            'claimant': 'Requester name',
            'mandatory': 'Is this related to a Fellows Inaugural meeting or Collaborations Workshop?',
            'title': 'Event title',
            'url': 'Event webpage link',
            'country': 'Country in which event is taking place',
            'city': 'City in which the event is taking place',
            'start_date': 'Start date of event (YYYY-MM-DD)',
            'end_date': 'End date of event (YYYY-MM-DD)',
            'budget_request_travel': "Travel costs (e.g. airfare or ground transportation)",
            'budget_request_attendance_fees': "Attendance fees (e.g. workshop / event registration costs)",
            'budget_request_subsistence_cost': "Subsistence costs (e.g. accommodation and meals)",
            'budget_request_venue_hire': "Venue hire",
            'budget_request_catering': "Catering",
            'budget_request_others': "Other costs",
            'direct_invoice': "Will expenses related to this request require a purchase order?",
            'justification': "For requests from individual £3000 Fellowship awards, please justify how this activity is in scope of your proposed Fellowship plans or how it furthers your goals for the Fellowship. For requests from the communal pot of funding, please justify how this activity supports the goals of the Institute (https://software.ac.uk/about). For requests relating to a Fellows Inaugural Meeting or Collaborations Workshop, please give a brief justification for the request.",
            'success_targeted': "Please specify what outputs (what may be produced) and outcomes (what change it could lead to) are likely to be produced from your participation in this event. These can include learning goals being met, collaborations, reports etc.",
            'additional_info': "Please specify details and breakdown of the costs. For example, indicating the mode(s) of travel and its associated cost. You can also add any other additional information here.",
            'can_be_advertise_before': "Can we publicly promote your involvement in this event before it takes place?",
            'can_be_advertise_after': "Can we publicly promote your involvement in this event after it takes place?"
        }

        widgets = {
            'claimant': Select(attrs={"class": "select-single-item"}),
            'category': Select(attrs={"class": "select-single-item"}),
            'focus': Select(attrs={"class": "select-single-item"}),
            'country': Select(attrs={"class": "select-single-item"}),
            'start_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
            'end_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
        }

    required_css_class = 'form-field-required'
    total_budget = CharField(required=False)

    # def clean_start_date(self):
    #     if 'start_date' in self.cleaned_data:
    #         date_from_today = self.cleaned_data['start_date'] - date.today()
    #         if date_from_today.days <= 0:
    #             raise ValidationError('"Start date of event" must be in the future.')
    #     return self.cleaned_data['start_date']

    def clean_end_date(self):
        # if 'end_date' in self.cleaned_data:
        #     date_from_today = self.cleaned_data['end_date'] - date.today()
        #     if date_from_today.days <= 0:
        #         raise ValidationError('"End date of event" must be in the future.')
        if 'start_date' in self.cleaned_data and 'end_date' in self.cleaned_data:
            duration = self.cleaned_data['end_date'] - self.cleaned_data['start_date']
            if duration.days < 0:
                raise ValidationError('"End date of event" must be after "Start date of event".')
        return self.cleaned_data['end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['additional_info'].required = True

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<p>To apply for expenses for eligible events, please fill in this form at least one month before the start date of the event you wish to attend or organise.</p><p>The application will then be reviewed by the Management team, and the Fellow will be informed by email (normally within two weeks) whether the application is successful (the Fellow may be contacted for further information before a decision is made).</p><p>Once the request is approved, the Fellow pays for their expenses and collects receipts and proofs of payment (e.g. bank/card statements) for all expenses incurred. Please note: If the Fellow requires support with costs up front (for example, such as invoices directly between the supplier and the Institute), then the Fellow needs to contact the Management team before submitting a funding request to find out what is possible. Setting up suppliers can take up to two months, so we recommend the Fellow gets in contact to discuss well before this.</p><p>After the activity is completed, the Fellow submits their associated <a href="https://fellows.software.ac.uk/blog/">blog post(s)</a> and <a href="https://fellows.software.ac.uk/expense/">expense claim(s)</a>.</p><h2>Requester details</h2>'),
                'claimant',
                HTML('<h2>Funding request details</h2>'),
                'category',
                'focus',
                'mandatory',
                'title',
                'url',
                'country',
                'city',
                'start_date',
                'end_date',
                HTML('''
                <h2>Costs</h2>
                <p>Please provide an estimate of your costs below. All values should be entered in GBP. See the terms and conditions for details (<a href="{{ terms_and_conditions_url }}">{{ terms_and_conditions_url }}</a>).</p>
                <p>Please fill in all cost sections that are relevant to your event type.</p>
                <p>You <strong>must</strong> include a cost breakdown in the <strong>"Additional information</strong>" section at the end of the form.</p>
                '''),
                PrependedText(
                    'budget_request_travel',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_attendance_fees',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_subsistence_cost',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_venue_hire',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_catering',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_others',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'total_budget',
                    '£',
                    disabled=True,
                    value=0.00
                ),
                HTML('<h2>Is a Purchase Order Required?</h2><p>If the payment is for a third-party organisation or individual, a purchase order (PO) may be required. If a PO is required, this must be raised <b>before</b> the event takes place.</p><p>For us to raise a PO, we need to know who we are paying (name/address etc.), what we are buying and how much it is going to cost e.g. Catering for an event on 28th May for 20 people, costing £160 plus VAT, provided by XYZ Catering.</p><p>If the supplier already exists on our system, there should be minimal delay in getting the PO issued.  If the supplier is a new supplier, the accounts payable team will contact the supplier for additional information, and it can take up to 3 months for the PO to be issued.</p><p>If you are paying an individual to reimburse their out-of-pocket expenses, this is done after the event using a simple claim form, but <b>you</b> need to upload the claim form onto lowFAT as it will be offset against your funding request.  It can take up to six weeks for these expenses to be reimbursed.</p><p>If you are paying an individual for their time e.g. 3 hours at £30 per hour to provide training or a workshop, this is treated by the University of Edinburgh as an appointment or engagement and requires an Employment Status Check to be completed <b>before</b> any work is started. It can take up to 3 months for the Employment Status Check to be completed.  Any work undertaken before these checks are completed will not be paid.  The way the payment is made depends on the outcome of these checks. The person undertaking this work will be required to have registered with HMRC for self assessment tax and must be able to provide a Unique Tax Reference No (UTR). Again, <b>you</b> should upload the claim form to lowFAT as it will be offset against your funding request.</p><p><b>Please make sure you tick the box below if a purchase order may be required</b></p>'),
                'direct_invoice',
                HTML('<h2>Justification for attending or organising the event</h2><p>When filling in the questions below please consider the following points:</p><ul><li>For attending conferences/workshops: will the conference focus on a significant field, will you meet significant researchers, will there be a focus on research software?</li><li>For organising workshops: how will the event help your domain, how will the event help the Institute, how will the event help you?</li><li>For policy related work: how might participation or organisation help the policy goals of the Institute, such as improving software and improved research (this can include people and tools perspectives)?</li><li>For other: please state reasons - note it may be good to discuss with the Institute Community Team before filling the form to make sure the rationale is aligned to the Institute and to your own objectives.</li></ul>'),
                HTML('<h4>Justification</h4>'),
                'justification',
                HTML('<h4>Successful outputs and outcomes</h4>'),
                'success_targeted',
                HTML('<h2>Details of people being sponsored from your Fellowship funds</h2><p>If you are sponsoring others to take part in this event from your Fellowship funds please give their names and email addresses below.  If you do not know their names at this stage please state whether there is sponsorship of others needed in this request. In either case please provide some justification.</p>'),
                'extra_sponsored',
                HTML('<h2>Additional information</h2>'),
                'additional_info',
                HTML('<h4>Publicity</h4>'),
                'can_be_advertise_before',
                'can_be_advertise_after',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )

        # Force user to select one category
        self.fields['category'].widget.choices.insert(0, ('', '---------'))
        self.fields['category'].initial = ''

        # Force user to select one focus
        self.fields['focus'].widget.choices.insert(0, ('', '---------'))
        self.fields['focus'].initial = ''


class FundPublicForm(GarlicForm):
    forenames = CharField(
        max_length=models.MAX_CHAR_LENGTH,
        required=True
    )
    surname = CharField(
        max_length=models.MAX_CHAR_LENGTH,
        required=True
    )
    email = EmailField(
        required=True
    )
    phone = CharField(
        max_length=models.MAX_CHAR_LENGTH,
        required=True,
        help_text="The number that we can contact you."
    )
    # gender = CharField(
    #     choices=GENDERS,
    #     max_length=1,
    #     default="R"
    # )
    # home_country = CountryField(
    #     required=True,
    #     default='GB'  # Default for United Kingdom
    # )
    home_city = CharField(
        required=True,
        max_length=models.MAX_CHAR_LENGTH
    )
    affiliation = CharField(  # Home institution
        max_length=models.MAX_CHAR_LENGTH,
        required=True,
    )
    department = CharField(  # Department within home institution
        max_length=models.MAX_CHAR_LENGTH,
        required=True
    )

    class Meta:
        model = models.Fund
        exclude = [  # pylint: disable=modelform-uses-exclude
            'claimant',
            'mandatory',
            'additional_info',
            'extra_sponsored',
            'can_be_included_in_calendar',
            'can_be_advertise_before',
            'can_be_advertise_after',
            "status",
            "ad_status",
            "budget_approved",
            "required_blog_posts",
            "grant_heading",
            "grant",
            "notes_from_admin",
            "added",
            "approved",
            "updated",
            "approval_chain",
        ]

        labels = {
            'mandatory': 'Is this related with Fellows face to face selection meeting, Fellows inaugural meeting or Collaborations Workshop?',
            'title': 'Event title',
            'url': 'Event webpage link',
            'country': 'Country in which event is taking place',
            'city': 'City in which the event is taking place',
            'start_date': 'Start date of event',
            'end_date': 'End date of event',
            'budget_request_travel': "Travel costs (e.g. airfare or ground transportation)",
            'budget_request_attendance_fees': "Attendance fees (e.g. workshop / event registration costs)",
            'budget_request_subsistence_cost': "Subsistence costs (e.g. accommodation and meals)",
            'budget_request_venue_hire': "Venue hire",
            'budget_request_catering': "Catering",
            'budget_request_others': "Other costs",
            'success_targeted': "Successful outputs and outcomes",
            'can_be_included_in_calendar': "Can we include your participation in this event into the private Fellows calendar?",
            'can_be_advertise_before': "Can we public promote your involvement in this event before it takes place?",
            'can_be_advertise_after': "Can we public promote your involvement in this event after it takes place?"
        }

        widgets = {
            'claimant': Select(attrs={"class": "select-single-item"}),
            'category': Select(attrs={"class": "select-single-item"}),
            'focus': Select(attrs={"class": "select-single-item"}),
            'country': Select(attrs={"class": "select-single-item"}),
            'start_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
            'end_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
        }

    required_css_class = 'form-field-required'
    total_budget = CharField(required=False)

    # def clean_start_date(self):
    #     if 'start_date' in self.cleaned_data:
    #         date_from_today = self.cleaned_data['start_date'] - date.today()
    #         if date_from_today.days <= 0:
    #             raise ValidationError('"Start date of event" must be in the future.')
    #     return self.cleaned_data['start_date']

    def clean_end_date(self):
        # if 'end_date' in self.cleaned_data:
        #     date_from_today = self.cleaned_data['end_date'] - date.today()
        #     if date_from_today.days <= 0:
        #         raise ValidationError('"End date of event" must be in the future.')
        if 'start_date' in self.cleaned_data and 'end_date' in self.cleaned_data:
            duration = self.cleaned_data['end_date'] - self.cleaned_data['start_date']
            if duration.days < 0:
                raise ValidationError('"End date of event" must be after "Start date of event".')
        return self.cleaned_data['end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<h2>Your details</h2>'),
                'forenames',
                'surname',
                # 'gender',
                'email',
                'phone',
                'home_city',
                # 'home_country',
                'affiliation',
                'department',
                HTML('<h2>Funding request details</h2>'),
                'category',
                'focus',
                'title',
                'url',
                'country',
                'city',
                'start_date',
                'end_date',
                HTML('<h2>Costs</h2><p>Please provide an estimate of your costs below. All values should be entered in GBP. See the terms and conditions for details (<a href="{{ terms_and_conditions_url }}">{{ terms_and_conditions_url }}</a>)</p><p>Please fill in all cost sections that are relevant to your event type.</p>'),
                PrependedText(
                    'budget_request_travel',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_attendance_fees',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_subsistence_cost',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_venue_hire',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_catering',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'budget_request_others',
                    '£',
                    onblur="update_budget()",
                    min=0.00,
                    step=0.01
                ),
                PrependedText(
                    'total_budget',
                    '£',
                    disabled=True,
                    value=0.00
                ),
                HTML('<h2>Justification for attending or organising the event</h2><p>When filling in the questions below please consider the following points:</p><ul><li>For attending conferences/workshops: will the conference focus on a significant field, will you meet significant researchers, will there be a focus on research software?</li><li>For organising workshops: how will the event help your domain, how will the event help the Institute, how will the event help you.</li><li>For policy related work: how might participation or organisation help the policy goals of the Institute, such as improving software and improved research (this can include people and tools perspectives).</li><li>For other: please state reasons - note it maybe good to discuss matter with the Institute Community Lead before filling the form to make sure the rationale is aligned to the Institute and to your own objectives.</li></ul>'),
                'justification',
                'success_targeted',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )

        # Force user to select one category
        self.fields['category'].widget.choices.insert(0, ('', '---------'))
        self.fields['category'].initial = ''

        # Force user to select one focus
        self.fields['focus'].widget.choices.insert(0, ('', '---------'))
        self.fields['focus'].initial = ''


class FundGDPRForm(GarlicForm):
    class Meta:
        model = models.Fund
        fields = [
            'can_be_included_in_calendar',
            'can_be_advertise_before',
            'can_be_advertise_after',
        ]

        labels = {
            'can_be_included_in_calendar': "Can we include your participation in this event into the Fellows calendar?",
            'can_be_advertise_before': "Can we public promote your involvement in this event before it takes place?",
            'can_be_advertise_after': "Can we public promote your involvement in this event after it takes place?"
        }

    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML('<h2>GDPR</h2>'),
                HTML('<h3>Publicity</h3>'),
                'can_be_advertise_before',
                'can_be_advertise_after',
                'can_be_included_in_calendar',
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )


class FundReviewForm(GarlicForm):
    class Meta:
        model = models.Fund
        fields = [
            "status",
            # "ad_status",  # TODO uncomment in the future
            "category",
            "focus",
            "mandatory",
            "grant_heading",
            "grant",
            "activity",
            "required_blog_posts",
            "budget_approved",
            "notes_from_admin",
        ]

        labels = {
            "mandatory": "Is this a mandatory event?",
            "grant_heading": "Default Grant Heading",
            "grant": "Default Grant",
            "activity": "Activities tag",
            'budget_approved': 'Total budget approved',
        }

    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                "status",
                "category",
                "focus",
                "mandatory",
                "grant",
                "grant_heading",
                "activity",
                HTML("""Visit <a href="/pages/guide/activities-tag/">Activities Tag Taxonomy</a> for a description about the tags."""),
                "required_blog_posts",
                PrependedText(
                    "budget_approved",
                    '£',
                    min=0.00,
                    step=0.01,
                    onblur="this.value = parseFloat(this.value).toFixed(2);"
                ),
                "notes_from_admin",
                "email",
                'not_send_email_field' if self.is_staff else None,
                'not_copy_email_field' if self.is_staff else None,
            )
        )

        self.helper.add_input(Submit('submit', 'Submit'))


class FundImportForm(Form):
    required_css_class = 'form-field-required'
    csv = FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
<li>Event title</li>
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
    form_complete = BooleanField(
        widget=CheckboxInput,
        required=True,
        initial=False,
        label="Have you filled out sections 1-4 and signed the form?"
    )

    items_listed = BooleanField(
        widget=CheckboxInput,
        required=True,
        initial=False,
        label="Have you listed and numbered each item you are claiming for so it matches a receipt?"
    )

    payment_proof = BooleanField(
        widget=CheckboxInput,
        required=True,
        initial=False,
        label="Have you included a proper proof of payment in the form of a formal receipt or invoice (preferably a VAT invoice) for each expense you are claiming for? "
    )

    bank_statement = BooleanField(
        widget=CheckboxInput,
        required=False,
        initial=False,
        label="In case of a foreign currency payment or a hotel booking, have you included your bank statement to show the exact amount deducted from your account?"
    )

    class Meta:
        model = models.Expense
        fields = [
            'fund',
            'claim',
            'receipts',
            'supporting_docs',
            'amount_claimed',
            'justification_for_extra',
            'invoice',
            'final',
            'advance_booking',
            'recipient_fullname',
            'recipient_email',
            'recipient_affiliation',
            'recipient_group',
            'recipient_connection',
        ]

        labels = {
            'fund': 'Choose approved funding request',
            'claim': 'Upload completed claim form (.docx file preferred)',
            'receipts': 'Upload PDF copy of receipt(s) and proof(s) of payment',
            'supporting_docs': 'Upload supporting documentation if applicable',
            'justification_for_extra': "If the claim is greater by 20% than the amount requested please provide justification",
            'invoice': "Do you need to claim this expense via an invoice from your institution or company?",
            'final': "Is this the final expense claim associated with this funding request?",
            'recipient_fullname': "Full name",
            'recipient_email': "E-mail",
            'recipient_affiliation': "Affiliation",
            'recipient_group': "Group",
            'recipient_connection': "Reason for submitting the recipient claim",
        }

        widgets = {
            'fund': Select(attrs={"class": "select-single-item"}),
        }

    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                HTML("<p>If your funding request isn't on the drop down menu below please email us at <a href='mailto:fellows-management@software.ac.uk'>fellows-management@software.ac.uk</a>.</p>"),
                'fund',
                HTML(textwrap.dedent("""\
                    <p>
                      Before submitting your expense claim:
                      <ol>
                        <li>Please follow the <a href='https://www.software.ac.uk/guide/guidelines-reimbursement-expenses-supported-software-sustainability-institute'>Guidelines for reimbursement of expenses from the Software Sustainability Institute</a>.
                            <ul>
                                <li>The Fellowship Programme Terms and Conditions and the <a href="https://www.ed.ac.uk/sites/default/files/atoms/files/new_expenses_policy.docx">University of Edinburgh Finance Expenses Policy</a> apply to your claim.
                                </li>
                            </ul>
                        </li>
                        <li>You MUST fill out the University of Edinburgh Payment of Non-Staff Expenses form which can be downloaded from <a href='https://www.software.ac.uk/guide/guidelines-reimbursement-expenses-supported-software-sustainability-institute'>this page of the SSI website</a>.
                            <ul>
                                <li>Fill out Sections 1-4 (pages 1-2) and page 6.</li>
                                <li>Leave the visitor/student number blank.</li>
                                <li>State your Name and Home Address (not your Work Address).</li>
                                <li>Make sure you have filled out your bank details correctly and clearly.</li>
                                <li>Don’t forget to sign the claim form. Electronic signature is fine.</li>
                                <li>List and number each item so it matches a receipt (do not sum receipts into e.g. 'Meals').</li>
                            </ul>
                        </li>
                        <li>You MUST compile all receipts/proofs of payment as a single PDF file.
                            <ul>
                                <li>For each item claimed, a detailed payment receipt must be provided and numbered.</li>
                                <li>When purchasing goods or services from VAT registered business, a VAT receipt must be provided.</li>
                                <li>Credit or debit card receipts are not sufficient on their own. An accompanying itemised receipt is necessary.</li>
                                <li>Hotel booking confirmation is not accepted as proof of payment, even if it does show an advance payment. Instead, a VAT invoice subsequent to the stay should be obtained and provided.</li>
                                <li>Likewise, online order confirmation is not accepted as proof of payment, even if it does show an advance payment. Instead, a VAT invoice should be obtained and provided.</li>
                                <li>A statement of your credit card/bank account should be present in the following cases:</li>
                                    <ul>
                                        <li>For hotel bookings</li>
                                        <li>For Non-GBP reimbursements</li>
                                            <ul>
                                                <li>For payments done in another currency and to be reimbursed in GBP</li>
                                                <li>For payments done in any currency but to be reimbursed in a non-GBP account</li>
                                            </ul>
                                    </ul>
                            </ul>
                        </li>
                      </ol>
                    </p>""")),
                'claim',
                'form_complete',
                'receipts',
                'items_listed',
                'payment_proof',
                'bank_statement',
                'supporting_docs',
                PrependedText(
                    'amount_claimed',
                    '£',
                    min=0.00,
                    step=0.01,
                    onblur="this.value = parseFloat(this.value).toFixed(2);"
                ),
                HTML("{% if fund %}<p class='text-warning'>Note that you only have <strong>£{{ fund.expenses_claimed_left }}</strong> left.</p>{% endif %}"),
                'justification_for_extra',
                'invoice',
                'final',
                'advance_booking' if self.is_staff else None,
                HTML("<h2>Recipient</h2><p>Only fill this part if you are claiming this expense on behalf of someone.</p>"),
                'recipient_fullname',
                'recipient_email',
                'recipient_affiliation',
                'recipient_group',
                'recipient_connection',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )

        if "initial" in kwargs and "fund" in kwargs["initial"]:
            self.fields['fund'].queryset = models.Fund.objects.filter(id=kwargs["initial"]["fund"].id)
        else:
            self.fields['fund'].queryset = models.Fund.objects.filter(status__in=models.FUND_STATUS_APPROVED_SET)


class ExpenseShortlistedForm(GarlicForm):
    class Meta:
        model = models.Expense
        fields = [
            'fund',
            'claim',
            'receipts',
            'amount_claimed',
            'justification_for_extra',
        ]

        labels = {
            'fund': 'Choose approved funding request',
            'claim': 'Completed claim form',
            'receipts': 'PDF copy of receipt(s)',
            'justification_for_extra': "If the claim is greater by 20% than the amount requested please provide justification",
        }

        widgets = {
            'fund': Select(attrs={"class": "select-single-item"}),
        }

    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                HTML("</p>If your funding request isn't on the drop down menu above please email <a href='mailto:{{ config.FELLOWS_MANAGEMENT_EMAIL }}'>us</a>."),
                'claim',
                PrependedText(
                    'amount_claimed',
                    '£',
                    min=0.00,
                    step=0.01,
                    onblur="this.value = parseFloat(this.value).toFixed(2);"
                ),
                'justification_for_extra',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )

        self.fields['fund'].queryset = models.Fund.objects.filter(status__in=models.FUND_STATUS_APPROVED_SET)


class ExpenseReviewForm(GarlicForm):
    class Meta:
        model = models.Expense
        fields = [
            'status',
            'final',
            'asked_for_authorization_date',
            'send_to_finance_date',
            'amount_authorized_for_payment',
            'grant_heading',
            'grant',
            'upload_final_claim_form',
            'notes_from_admin',
        ]

        widgets = {
            'asked_for_authorization_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
            'send_to_finance_date': DatePickerInput(options={"format": "YYYY-MM-DD"}),
        }

    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'status',
                'final',
                'asked_for_authorization_date',
                'send_to_finance_date',
                PrependedText(
                    'amount_authorized_for_payment',
                    '£',
                    min=0.00,
                    step=0.01,
                    onblur="this.value = parseFloat(this.value).toFixed(2);"
                ),
                'upload_final_claim_form',
                'grant',
                'grant_heading',
                'notes_from_admin',
                'email',
                'not_send_email_field' if self.is_staff else None,
                'not_copy_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', 'Update')
                )
            )
        )


class BlogForm(GarlicForm):
    success_reported = CharField(
        widget=Textarea,
        required=False,
        initial="",
        label="What outputs were produced and which outcomes were achieved by your participation in the event."
    )

    class Meta:
        model = models.Blog
        fields = [
            'fund',
            'coauthor',
            'draft_url',
            'final',
            'notes_from_author',
        ]
        labels = {
            'fund': 'Open approved funding request',
            'coauthor': 'Co-author',
            'draft_url': 'URL of blog post draft',
            'final': "Is this the final blog post draft associated with this funding request?",
            'notes_from_author': "Notes"
        }

        widgets = {
            'fund': Select(attrs={"class": "select-single-item"}),
            'coauthor': SelectMultiple(attrs={"class": "select-many-item"}),
        }

    required_css_class = 'form-field-required'

    # workaround for "no such table: lowfat_claimant"
    try:
        author_choices = [(this_claimant.id, this_claimant) for this_claimant in models.Claimant.objects.all()]

    except:
        logger.warning('Exception caught by bare except')
        logger.warning('%s %s', *(sys.exc_info()[0:2]))

        author_choices = []
    author = ChoiceField(
        widget=Select(attrs={"class": "select-single-item"}),
        required=False,
        choices=author_choices,
        label='Main author of draft'
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                'final',
                'author' if self.is_staff else None,
                'coauthor',
                HTML(
                    "<p>For guidance on writing a blog post for the SSI website, please refer to the"
                    " <a href='https://software.ac.uk/resources/guides/guides-content-contributors'>Guides for content contributors.</a></p>"
                    "<p>We prefer to receive links to <a href='https://www.google.co.uk/docs/about/'>Google Docs</a>"
                    " (tips <a href='/pages/guide/google-docs/'>here</a>),"
                    " <a href='https://products.office.com/en-gb/office-365-home'>Microsoft Office 365 document</a>"
                    " or any other online live collaborative document platform you like to use."
                    " Posts published somewhere already, e.g. your personal blog, are welcome as well.</p>"),
                'draft_url',
                'success_reported',
                'notes_from_author',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
            )
        )

        if "initial" in kwargs and "fund" in kwargs["initial"]:
            self.fields['fund'].queryset = models.Fund.objects.filter(id=kwargs["initial"]["fund"].id)
        else:
            self.fields['fund'].queryset = models.Fund.objects.filter(status__in=models.FUND_STATUS_APPROVED_SET)

        if user:
            self.fields['fund'].queryset = models.Fund.objects.filter(status__in=models.FUND_STATUS_APPROVED_SET)

        if self.is_staff:
            # Force staff to select one author
            self.fields['author'].widget.choices.insert(0, ('', '---------'))
            self.fields['author'].initial = ''


class BlogReviewForm(GarlicForm):
    class Meta:
        model = models.Blog
        exclude = [  # pylint: disable=modelform-uses-exclude
            "fund",
            "author",
            "coauthor",
            "notes_from_author",
            "added",
            "updated",
        ]

    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'draft_url',
                'final',
                'status',
                'reviewer',
                'notes_from_admin',
                'published_url',
                'title',
                'tweet_url',
                'email',
                'not_send_email_field' if self.is_staff else None,
                'not_copy_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', 'Update')
                )
            )
        )

        self.fields['reviewer'].queryset = get_user_model().objects.filter(
            is_staff=True)
