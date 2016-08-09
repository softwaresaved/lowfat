from datetime import date
import uuid

import django.utils
from django.conf import settings
from django.db import models

from django_countries.fields import CountryField

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

EVENT_CATEGORY = (
        ('A', 'Attending a conference/workshop'),
        ('H', 'Organising a conference/workshop (e.g. Software Carpentry)'),
        ('P', 'Policy related event'),
        ('O', 'Other'),
        )

AD_STATUS = (
        ('U', 'Unprocessed'),  # Initial status
        ('V', 'Visible'),  # Event is visible on map
        ('H', 'Hide'),  # Event is invisible on map
        )

EVENT_STATUS = (
        ('U', 'Unprocessed'),  # Initial status
        ('P', 'Processing'),  # When someone was assigned to review the request
        ('A', 'Approved'),  # Event was approved. Funds are reserved.
        ('R', 'Reproved'),  # Event was declided.
        ('F', 'Archived'),  # Approved events with all claims and blog posts were processed. No funds are reserved.
        )

EXPENSE_STATUS = (
        ('W', 'Not submitted yet'),
        ('S', 'Submitted (but not processed yet)'),
        ('P', 'Processing'),
        ('A', 'Approved (waiting reply from finances)'),
        ('F', 'Finished'),
        )

FUNDS_FROM = (
    ('C', 'Continuing (fellowship)'),
    ('I', 'Core (Software Sustainability Institute)'),
    ('F', 'Grant (inauguration fellowship)'),
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


class Fellow(models.Model):
    """Describe a fellow."""

    class Meta:
        app_label = 'fat'

    # Authentication
    #
    # We use this to only allow fellow to access their own data.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            null=True,
            blank=True)

    # Personal info (application details)
    forenames = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    surname = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    email = models.EmailField(
            blank=False)
    phone = models.CharField(max_length=MAX_CHAR_LENGTH,
                             blank=False,
                             help_text="The number that we can contact you.",
    )
    gender = models.CharField(choices=GENDERS,
            max_length=1,
            default="R")
    home_country = CountryField(
        blank=False,
        default='GB')  # Default for United Kingdom
    home_city = models.CharField(
        blank=False,
        max_length=MAX_CHAR_LENGTH)
    home_lon = models.FloatField(
            null=True,
            blank=True)
    home_lat = models.FloatField(
            null=True,
            blank=True)
    photo = models.FileField(
            upload_to='photos/',  # File will be uploaded to MEDIA_ROOT/photos
            null=True,
            blank=True)  # This need to be a JPG.

    # Professional info
    # JACS code for research_area.
    # https://www.hesa.ac.uk/jacs/
    research_area = models.TextField(
        help_text="Please describe your research"
    )
    research_area_code = models.CharField(choices=JACS_LEVEL_2,
                                          max_length=4,
                                          default="Y000")
    affiliation = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    funding = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    funding_notes = models.TextField(
            null=True,
            blank=True)
    work_description = models.TextField(blank=False)

    # Social media
    website = models.URLField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    website_feed = models.URLField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    orcid = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    github = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    gitlab = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    twitter = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    facebook = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)

    # Admin fields
    application_year = models.IntegerField(
                null=False,
                blank=False,
                default=date.today().year)
    selected = models.BooleanField(default=False)
    fellowship_grant = models.DecimalField(max_digits=MAX_DIGITS,
                                           decimal_places=2,
                                           null=False,
                                           blank=False,
                                           default=0.00)
    notes_from_admin = models.TextField(
            null=True,
            blank=True)

    # Mentors need to be another fellow
    mentor = models.ForeignKey('self',
            blank=True,
            null=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.forenames, self.surname)

    def fellowship_available(self):
        """Return the remain fellowship grant."""
        return self.fellowship_grant - self.fellowship_spent() - self.fellowship_remaining()

    def fellowship_committed(self):
        """Return the ammount committed from the fellowship grant."""
        this_fellow_events = Event.objects.filter(fellow=self, status__in=['A', 'F'])
        return sum([event.budget_approved for event in this_fellow_events])

    def fellowship_spent(self):
        """Return the ammount alread spent from the fellowship grant."""
        this_fellow_expenses = Expense.objects.filter(event__fellow=self, status__in=['A', 'F']).exclude(funds_from__in=["C", "I"])
        return sum([expense.amount_claimed for expense in this_fellow_expenses])

    def fellowship_remaining(self):
        """Return the ammount remaining to claim from the total committed."""
        this_fellow_events = Event.objects.filter(fellow=self, status__in=['U', 'P', 'A'])
        return self.fellowship_committed() - self.fellowship_spent()



class Event(models.Model):
    """Describe a event from one fellow."""
    class Meta:
        app_label = 'fat'

    # TODO Make fellow more generic to include staffs.
    fellow = models.ForeignKey('Fellow')
    category = models.CharField(choices=EVENT_CATEGORY,
            max_length=1,
            default="O")
    name = models.CharField(max_length=MAX_CHAR_LENGTH)
    url = models.URLField(max_length=MAX_CHAR_LENGTH)
    country = CountryField(default='GB')  # Default for United Kingdom
    city = models.CharField(max_length=MAX_CHAR_LENGTH)
    lon = models.FloatField(
            null=True,
            blank=True)
    lat = models.FloatField(
            null=True,
            blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget_request_travel = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_request_attendance_fees = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_request_subsistence_cost = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_request_venue_hire = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_request_catering = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_request_others = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)
    budget_approved = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            default=0.00)    
    justification = models.TextField()
    additional_info = models.TextField(blank=True)
    extra_sponsored = models.TextField(blank=True)
    can_be_advertise_before = models.BooleanField(default=False)
    can_be_advertise_after = models.BooleanField(default=False)

    # Admin fields
    ad_status = models.CharField(choices=AD_STATUS,
            max_length=1,
            default="U")
    status = models.CharField(choices=EVENT_STATUS,
            max_length=1,
            default="U")
    required_blog_posts = models.IntegerField(
                null=False,
                blank=False,
                default=1)
    notes_from_admin = models.TextField(
            null=True,
            blank=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{}".format(self.name)

    def budget_total(self):
        """Return the sum of all `budget_request`s."""
        return sum([
                self.budget_request_travel,
                self.budget_request_attendance_fees,
                self.budget_request_subsistence_cost,
                self.budget_request_venue_hire,
                self.budget_request_catering,
                self.budget_request_others,
                ])

    def expenses_claimed(self):
        """Return the total ammount of expenses claimed."""
        this_event_expenses = Expense.objects.filter(event=self)
        return sum([expense.amount_claimed for expense in this_event_expenses])

    def expenses_authorized_for_payment(self):
        """Return the total ammount of expenses authorized_for_payment."""
        this_event_expenses = Expense.objects.filter(event=self)
        return sum([expense.amount_authorized_for_payment for expense in this_event_expenses])

    def total_of_blog_posts(self):
        """Return number of blog posts."""
        return Blog.objects.filter(event=self).count()


class Expense(models.Model):
    """This describe one expense for one event."""
    class Meta:
        app_label = 'fat'

    # Hash for id to avoid leak of information
    id = models.UUIDField(primary_key=True,
            default=uuid.uuid4,
            editable=False)

    # Form
    event = models.ForeignKey('Event')
    claim = models.FileField(
            upload_to='expenses/'  # File will be uploaded to MEDIA_ROOT/expenses
        )
    amount_claimed = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    recipient = models.TextField(
        blank=True,
        help_text="Keep empty if the recipient is the fellow."
    )
    final = models.BooleanField(
        default=False,
        help_text="This is your last expense claim for the event"
    )

    # Admin fields
    status = models.CharField(choices=EXPENSE_STATUS,
            max_length=1,
            default="P")
    received_date = models.DateField(default=django.utils.timezone.now)
    asked_for_authorization_date = models.DateField(
        blank=True,
        null=True
    )
    send_to_finance_date = models.DateField(
        blank=True,
        null=True
    )
    amount_authorized_for_payment = models.DecimalField(max_digits=MAX_DIGITS,
                                 decimal_places=2,
                                 blank=False,
                                 default=0.00)
    funds_from = models.CharField(choices=FUNDS_FROM,
            max_length=1,
            default="C")
    grant_used = models.CharField(choices=GRANTS,
            max_length=4,
            default="SS2")
    notes_from_admin = models.TextField(
            null=True,
            blank=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.claim.name


class Blog(models.Model):
    """Provide the link to the blog post about the event."""
    class Meta:
        app_label = 'fat'

    # Form
    event = models.ForeignKey('Event')
    draft_url = models.URLField(max_length=MAX_CHAR_LENGTH)
    final = models.BooleanField(
        default=False,
        help_text="This is your last blog post about the event"
    )

    # Admin fields
    status = models.CharField(choices=BLOG_POST_STATUS,
            max_length=1,
            default="U")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
            null=True,
            blank=True)
    notes_from_admin = models.TextField(
            null=True,
            blank=True)
    published_url = models.URLField(max_length=MAX_CHAR_LENGTH,
            null=True,
            blank=True)
    tweet_url = models.URLField(max_length=MAX_CHAR_LENGTH,
            null=True,
            blank=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.published_url:
            self.status = 'P'
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.draft_url)
