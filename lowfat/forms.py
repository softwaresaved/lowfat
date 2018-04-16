from datetime import datetime

from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    ChoiceField,
    FileField,
    Form,
    ModelForm,
    Select,
    SelectMultiple,
    Textarea,
)

from datetimewidget.widgets import DateWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import PrependedText

from .models import *

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
            'career_stage_when_apply',
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
                'career_stage_when_apply',
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
            'photo_work_description',
            'career_stage_when_apply',
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
                'photo_work_description',
                'photo',
                HTML('<h2>Professional details</h2>'),
                'career_stage_when_apply',
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


class FundForm(GarlicForm):
    class Meta:
        model = Fund
        exclude = [
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
        ]

        labels = {
            'claimant': 'Requester name',
            'mandatory': 'Is this related with Fellows face to face selection meeting, Fellows inaugural meeting or Collaborations Workshop?',
            'title': 'Event title',
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
            'claimant': Select(attrs={"class": "select-single-item"}),
            'category': Select(attrs={"class": "select-single-item"}),
            'focus': Select(attrs={"class": "select-single-item"}),
            'country': Select(attrs={"class": "select-single-item"}),
            'start_date': DateWidget(
                usel10n=True,
                bootstrap_version=3
            ),
            'end_date': DateWidget(
                usel10n=True,
                bootstrap_version=3
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
                'focus',
                'mandatory',
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
                'additional_info',
                HTML('<h2>Details of people being sponsored from your Fellowship funds</h2><p>If you are sponsoring others to take part in this event from your Fellowship funds please give their names and email addresses below, if you do not know their names at this stage please state whether there is sponsorship of others needed in this request. In either case please provide some justification.</p>'),
                'extra_sponsored',
                HTML('<h2>Publicity</h2>'),
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


class FundReviewForm(GarlicForm):
    class Meta:
        model = Fund
        fields = [
            "status",
            #"ad_status",  # TODO uncomment in the future
            "grant_heading",
            "grant",
            "activity",
            "required_blog_posts",
            "budget_approved",
            "notes_from_admin",
        ]

        labels = {
            "grant_heading": "Default Grant Heading",
            "grant": "Default Grant",
            "activity": "Activities tag",
            'budget_approved': 'Total budget approved',
        }


    required_css_class = 'form-field-required'
    email = CharField(widget=Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(FundReviewForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                "status",
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
    class Meta:
        model = Expense
        fields = [
            'fund',
            'claim',
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
            'claim': 'PDF copy of claim and receipt(s)',
            'justification_for_extra': "If the claim is greater by 20% than the amount requested please provide justification",
            'invoice': "Do you need to claim this expense via an invoice from your institution or company?",
            'final': "Is this the final expense claim associated with this funding request?",
            'recipient_fullname': "Full name",
            'recipient_email': "E-mail",
            'recipient_affiliation': "Affiliation",
            'recipient_group': "Group",
            'recipient_connection': "Reason for submit the recipient claim",
        }

        widgets = {
            'fund': Select(attrs={"class": "select-single-item"}),
        }


    required_css_class = 'form-field-required'

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                HTML("</p>If your funding request isn't on the drop down menu above please email <a href='mailto:{{ config.FELLOWS_MANAGEMENT_EMAIL }}'>us</a>."),
                HTML("</p><a href='{{ terms_and_conditions_url }}'>Fellowship Programme's terms and conditions</a> applies to your request. Please follow the guidelines at <a href='{{ terms_and_conditions_url }}#how-to-apply-for-and-claim-expenses'>How to apply for, and claim, expenses</a> section of <a href='{{ terms_and_conditions_url }}'>Fellowship Programme's terms and conditions.</a></p>"),
                'claim',
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
                HTML("<p>You need to provide a reason for submit the recipient claim. An common reasons is \"because the recipient was of of the speakers on that workshop\".</p>"),
                'recipient_connection',
                'not_send_email_field' if self.is_staff else None,
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
            'asked_for_authorization_date',
            'send_to_finance_date',
            'amount_authorized_for_payment',
            'grant_heading',
            'grant',
            'notes_from_admin',
        ]

        widgets = {
            'asked_for_authorization_date': DateWidget(
                usel10n=True,
                bootstrap_version=3
            ),
            'send_to_finance_date': DateWidget(
                usel10n=True,
                bootstrap_version=3
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
                'asked_for_authorization_date',
                'send_to_finance_date',
                PrependedText(
                    'amount_authorized_for_payment',
                    '£',
                    min=0.00,
                    step=0.01,
                    onblur="this.value = parseFloat(this.value).toFixed(2);"
                ),
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
    class Meta:
        model = Blog
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
        author_choices = [(this_claimant.id, this_claimant) for this_claimant in Claimant.objects.all()]
    except:  # pylint: disable=bare-except
        author_choices = []
    author = ChoiceField(
        widget=Select(attrs={"class": "select-single-item"}),
        required=False,
        choices=author_choices,
        label='Main author of draft'
    )


    def __init__(self, *args, user=None, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset(
                '',
                'fund',
                'author' if self.is_staff else None,
                'coauthor',
                HTML("<p>We prefer to receive links to <a href='https://www.google.co.uk/docs/about/'>Google Docs</a> (tips <a href='/pages/guide/google-docs/'>here</a>), <a href='https://products.office.com/en-gb/office-365-home'>Microsoft Office 365 document</a> or any other online live collaborative document platform you like to use. Posts published somewhere already, e.g. your personal blog, are welcome as well.</p>"),
                'draft_url',
                HTML('<p>To apply for expenses for eligible events, please fill in this form at least one month before the start date of the event you wish to attend or organise.</p><h2>Requester details</h2>'),
                'final',
                'notes_from_author',
                'not_send_email_field' if self.is_staff else None,
                ButtonHolder(
                    Submit('submit', '{{ title }}')
                )
                )
            )

        if user:
            self.fields['fund'].queryset = Fund.objects.filter(status__in=['A'])

        if self.is_staff:
            # Force staff to select one author
            self.fields['author'].widget.choices.insert(0, ('', '---------'))
            self.fields['author'].initial = ''


class BlogReviewForm(GarlicForm):
    class Meta:
        model = Blog
        exclude = [
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
        super(BlogReviewForm, self).__init__(*args, **kwargs)

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
