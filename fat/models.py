from datetime import date
import re

import django.utils
from django.conf import settings
from django.db import models

from django_countries.fields import CountryField

from .validator import pdf
from .jacs import JACS_LEVEL_2

MAX_CHAR_LENGTH = 120
MAX_PHONE_LENGTH = 14
MAX_DIGITS = 10

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('R', 'Rather not say'),
)

FUND_CATEGORY = (
    ('A', 'Attending a conference/workshop'),
    ('H', 'Organising a conference/workshop (e.g. Software Carpentry)'),
    ('P', 'Policy related event'),
    ('O', 'Other'),
)

AD_STATUS = (
    ('U', 'Unprocessed'),  # Initial status
    ('V', 'Visible'),  # Fund is visible on map
    ('H', 'Hide'),  # Fund is invisible on map
)

FUND_STATUS = (
    ('U', 'Unprocessed'),  # Initial status
    ('P', 'Processing'),  # When someone was assigned to review the request
    ('A', 'Approved'),  # Fund was approved. Funds are reserved.
    ('R', 'Reproved'),  # Fund was declided.
    ('F', 'Archived'),  # Approved funds with all claims and blog posts were processed. No funds are reserved.
    ('C', 'Canceled'),  # When the fellow decided to cancel their request.
)

FUND_STATUS_LONG_DESCRIPTION = {
    'U': "We didn't start to process your request yet.",
    'P': "One of your staffs is reviewing your request. You should have our reply soon.",
    'A': "Your fund request was approved.",
    'R': "Your fund request was declided.",
    'F': "We archived your fund request since all the expense claims were processed.",
    'C': "You decided to cancel this request for any reason.",
}


EXPENSE_STATUS = (
    ('W', 'Not submitted yet'),
    ('S', 'Submitted (awaiting processing)'),
    ('C', 'Administrator checking'),
    ('P', 'Authoriser checking'),
    ('A', 'Approved (submitted to finance)'),
    ('F', 'Finished'),
)

FUNDS_FROM = (
    ('C', 'Continuing (claimantship)'),
    ('I', 'Core (Software Sustainability Institute)'),
    ('F', 'Grant (inauguration claimantship)'),
)

GRANTS = (
    ('SSI1', 'Software Sustainability Institute - Phase 1'),
    ('SSI2', 'Software Sustainability Institute - Phase 2'),
    ('SSI3', 'Software Sustainability Institute - Phase 3'),
)

BLOG_POST_STATUS = (
    ('U', 'Unprocessed'),
    ('R', 'On Google Drive (for review)'),
    ('L', 'On pipeline to be published'),
    ('P', 'Published'),
    ('D', 'Declined'),
    ('O', 'Out of date'),
)

def fix_url(url):
    """Prepend 'http://' to URL."""
    if url is not None and url and not re.match("https?://", url):
        return "http://{}".format(url)

    return url

def slug_generator(forenames, surname):
    """Generate slug for Claimant"""
    return "{}-{}".format(
        forenames.lower().replace(" ", "-"),
        surname.lower().replace(" ", "-")
    )

class Claimant(models.Model):
    """Describe a claimant."""

    class Meta:
        app_label = 'fat'

    # Authentication
    #
    # We use this to only allow claimant to access their own data.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True
    )

    # Personal info (application details)
    forenames = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False
    )
    surname = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False
    )
    email = models.EmailField(
        blank=False
    )
    phone = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False,
        help_text="The number that we can contact you."
    )
    gender = models.CharField(
        choices=GENDERS,
        max_length=1,
        default="R"
    )
    home_country = CountryField(
        blank=False,
        default='GB'  # Default for United Kingdom
    )
    home_city = models.CharField(
        blank=False,
        max_length=MAX_CHAR_LENGTH
    )
    home_lon = models.FloatField(
        null=True,
        blank=True
    )
    home_lat = models.FloatField(
        null=True,
        blank=True
    )
    photo = models.FileField(
        upload_to='photos/',  # File will be uploaded to MEDIA_ROOT/photos
        null=True,
        blank=True  # This need to be a JPG.
    )

    # Professional info
    # JACS code for research_area.
    # https://www.hesa.ac.uk/jacs/
    research_area = models.TextField(
        blank=True,
        help_text="Please describe your research"
    )
    research_area_code = models.CharField(
        choices=JACS_LEVEL_2,
        max_length=4,
        default="Y000"
    )
    affiliation = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    funding = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    funding_notes = models.TextField(
        null=True,
        blank=True
    )
    work_description = models.TextField(blank=True)

    # Social media
    website = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    website_feed = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    orcid = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    github = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    gitlab = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    twitter = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    facebook = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )

    # Admin fields
    slug = models.CharField(max_length=MAX_CHAR_LENGTH)
    application_year = models.IntegerField(
        null=False,
        blank=False,
        default=date.today().year
    )
    selected = models.BooleanField(default=False)
    software_carpentry_instructor = models.BooleanField(default=False)
    data_carpentry_instructor = models.BooleanField(default=False)
    claimantship_grant = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.00
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )

    # Mentors need to be another claimant
    mentor = models.ForeignKey(
        'self',
        blank=True,
        null=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slug_generator(self.forenames, self.surname)
        self.website = fix_url(self.website)
        self.website_feed = fix_url(self.website)

        super(Claimant, self).save(*args, **kwargs)

    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.forenames, self.surname)

    def claimantship_available(self):
        """Return the remain claimantship grant."""
        return self.claimantship_grant - self.claimantship_spent() - self.claimantship_remaining()

    def claimantship_committed(self):
        """Return the ammount committed from the claimantship grant."""
        this_claimant_funds = Fund.objects.filter(
            claimant=self,
            status__in=['A', 'F']
        )
        return sum([fund.budget_approved for fund in this_claimant_funds])

    def claimantship_spent(self):
        """Return the ammount alread spent from the claimantship grant."""
        this_claimant_expenses = Expense.objects.filter(
            fund__claimant=self,
            status__in=['A', 'F']
        ).exclude(funds_from__in=["C", "I"])
        return sum([expense.amount_claimed for expense in this_claimant_expenses])

    def claimantship_remaining(self):
        """Return the ammount remaining to claim from the total committed."""
        return self.claimantship_committed() - self.claimantship_spent()


class Fund(models.Model):
    """Describe a fund from one claimant."""
    class Meta:
        app_label = 'fat'

    # TODO Make claimant more generic to include staffs.
    claimant = models.ForeignKey('Claimant')
    category = models.CharField(
        choices=FUND_CATEGORY,
        max_length=1,
        default="O"
    )
    category_other = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    url = models.CharField(max_length=MAX_CHAR_LENGTH)
    country = CountryField(default='GB')  # Default for United Kingdom
    city = models.CharField(max_length=MAX_CHAR_LENGTH)
    lon = models.FloatField(
        null=True,
        blank=True
    )
    lat = models.FloatField(
        null=True,
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    budget_request_travel = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_request_attendance_fees = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_request_subsistence_cost = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_request_venue_hire = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_request_catering = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_request_others = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    budget_approved = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        default=0.00
    )
    justification = models.TextField()
    additional_info = models.TextField(blank=True)
    extra_sponsored = models.TextField(blank=True)
    can_be_advertise_before = models.BooleanField(default=False)
    can_be_advertise_after = models.BooleanField(default=True)

    # Admin fields
    ad_status = models.CharField(
        choices=AD_STATUS,
        max_length=1,
        default="U"
    )
    status = models.CharField(
        choices=FUND_STATUS,
        max_length=1,
        default="U"
    )
    required_blog_posts = models.IntegerField(
        null=False,
        blank=False,
        default=1
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.url = fix_url(self.url)

        super(Fund, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)

    def status_help(self):
        """Provide long description for the status."""

        # XXX Propably there is a better way to do this.
        return FUND_STATUS_LONG_DESCRIPTION[self.status]

    def budget_total(self):
        """Return the sum of all `budget_request`s."""
        return sum(
            [
                self.budget_request_travel,
                self.budget_request_attendance_fees,
                self.budget_request_subsistence_cost,
                self.budget_request_venue_hire,
                self.budget_request_catering,
                self.budget_request_others,
            ]
        )

    def expenses_claimed(self):
        """Return the total ammount of expenses claimant."""
        this_fund_expenses = Expense.objects.filter(fund=self)
        return sum([expense.amount_claimed for expense in this_fund_expenses])

    def expenses_claimed_left(self):
        """Return the total ammount left to claimant."""
        this_fund_expenses = Expense.objects.filter(fund=self)
        return self.budget_total() - sum([expense.amount_claimed for expense in this_fund_expenses])

    def expenses_authorized_for_payment(self):
        """Return the total ammount of expenses authorized_for_payment."""
        this_fund_expenses = Expense.objects.filter(fund=self)
        return sum([expense.amount_authorized_for_payment for expense in this_fund_expenses])

    def total_of_blog_posts(self):
        """Return number of blog posts."""
        return Blog.objects.filter(fund=self).count()


class Expense(models.Model):
    """This describe one expense for one fund."""
    class Meta:
        app_label = 'fat'

    # Internal
    relative_number = models.IntegerField(
        null=False,
        blank=False
    )

    # Form
    fund = models.ForeignKey('Fund')
    claim = models.FileField(
        upload_to='expenses/',  # File will be uploaded to MEDIA_ROOT/expenses
        validators=[pdf]
    )
    amount_claimed = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        blank=False,
        default=0.00
    )
    justification_for_extra = models.TextField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    final = models.BooleanField(
        default=False
    )
    # Recipient
    recipient_fullname = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    recipient_email = models.EmailField(
        blank=True
    )
    recipient_affiliation = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    recipient_group = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    recipient_connection = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )

    # Admin fields
    status = models.CharField(
        choices=EXPENSE_STATUS,
        max_length=1,
        default="P"
    )
    received_date = models.DateField(default=django.utils.timezone.now)
    asked_for_authorization_date = models.DateField(
        blank=True,
        null=True
    )
    send_to_finance_date = models.DateField(
        blank=True,
        null=True
    )
    amount_authorized_for_payment = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        blank=False,
        default=0.00
    )
    funds_from = models.CharField(
        choices=FUNDS_FROM,
        max_length=1,
        default="C"
    )
    grant_used = models.CharField(
        choices=GRANTS,
        max_length=4,
        default="SS2"
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.claim.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            previous_number = Expense.objects.filter(fund=self.fund).count()
            self.relative_number = previous_number + 1
        super(Expense, self).save(*args, **kwargs)


class Blog(models.Model):
    """Provide the link to the blog post about the fund."""
    class Meta:
        app_label = 'fat'

    # Form
    fund = models.ForeignKey('Fund')
    draft_url = models.CharField(max_length=MAX_CHAR_LENGTH)
    final = models.BooleanField(
        default=False
    )

    # Admin fields
    status = models.CharField(
        choices=BLOG_POST_STATUS,
        max_length=1,
        default="U"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )
    published_url = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        null=True,
        blank=True
    )
    tweet_url = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        null=True,
        blank=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.draft_url = fix_url(self.draft_url)
        self.published_url = fix_url(self.published_url)
        self.tweet_url = fix_url(self.tweet_url)

        if self.published_url:
            self.status = 'P'
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.draft_url)

class GeneralSentMail(models.Model):
    """Emails sent with custom text."""

    class Meta:
        app_label = 'fat'

    justification = models.TextField()

    # Internal
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    receiver = models.ForeignKey('Claimant')


class FundSentMail(GeneralSentMail):
    fund = models.ForeignKey('Fund')


class ExpenseSentMail(GeneralSentMail):
    expense = models.ForeignKey('Expense')


class BlogSentMail(GeneralSentMail):
    blog = models.ForeignKey('Blog')
