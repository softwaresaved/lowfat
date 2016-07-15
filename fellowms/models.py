from datetime import date
import uuid

from django.conf import settings
from django.db import models

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
        app_label = 'fellowms'

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
            blank=False)
    gender = models.CharField(choices=GENDERS,
            max_length=1,
            default="R")
    home_location = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
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
            null=True,
            blank=True)
    research_area_code = models.CharField(max_length=4,
            blank=False)
    affiliation = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    funding = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    funding_notes = models.TextField(
            null=True,
            blank=True)
    work_description = models.TextField(blank=False)

    # Social media
    website = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    website_feed = models.CharField(max_length=MAX_CHAR_LENGTH,
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
        return "{} {}".format(self.forenames, self.surname)

    def fellowship_used(self):
        """Return the ammount alread used from the fellowship grant."""
        this_fellow_expenses = Expense.objects.filter(event__fellow=self, status__in=['A', 'F'])
        return sum([expense.amount_claimed for expense in this_fellow_expenses])

    def fellowship_reserve(self):
        """Return the ammount reserved from the fellowship grant."""
        this_fellow_events = Event.objects.filter(fellow=self, status__in=['U', 'P', 'A'])
        return sum([event.budget_approved if event.budget_approved else event.budget_total() for event in this_fellow_events])

    def fellowship_available(self):
        """Return the remain fellowship grant."""
        return self.fellowship_grant - self.fellowship_reserve() - self.fellowship_used()


class Event(models.Model):
    """Describe a event from one fellow."""
    class Meta:
        app_label = 'fellowms'

    fellow = models.ForeignKey('Fellow',
            null=True,
            blank=True)
    category = models.CharField(choices=EVENT_CATEGORY,
            max_length=1,
            default="O")
    name = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    url = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    location = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True)
    lon = models.FloatField(
            null=True,
            blank=True)
    lat = models.FloatField(
            null=True,
            blank=True)
    start_date = models.DateField(
            blank=True,
            null=True)
    end_date = models.DateField(blank=True, null=True)
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
    justification = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)

    # Admin fields
    ad_status = models.CharField(choices=AD_STATUS,
            max_length=1,
            default="U")
    status = models.CharField(choices=EVENT_STATUS,
            max_length=1,
            default="U")
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


class Expense(models.Model):
    """This describe one expense for one event."""
    class Meta:
        app_label = 'fellowms'

    # Hash for id to avoid leak of information
    id = models.UUIDField(primary_key=True,
            default=uuid.uuid4,
            editable=False)

    # Form
    event = models.ForeignKey('Event',
            null=False,
            blank=False)
    proof = models.FileField(
            upload_to='expenses/',  # File will be uploaded to MEDIA_ROOT/expenses
            null=True,
            blank=True)  # This need to be a PDF.
    amount_claimed = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)

    # Admin fields
    status = models.CharField(choices=EXPENSE_STATUS,
            max_length=1,
            default="P")
    amount_authorized_for_payment = models.DecimalField(max_digits=MAX_DIGITS,
                                 decimal_places=2,
                                 blank=False,
                                 default=0.00)
    funds_from = models.CharField(choices=FUNDS_FROM,
            max_length=1,
            default="C")
    notes_from_admin = models.TextField(
            null=True,
            blank=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.proof.name


class Blog(models.Model):
    """Provide the link to the blog post about the event."""
    class Meta:
        app_label = 'fellowms'

    event = models.ForeignKey('Event',
            null=False,
            blank=False)
    draft_url = models.CharField(max_length=MAX_CHAR_LENGTH,
                blank=False)
    status = models.CharField(choices=BLOG_POST_STATUS,
            max_length=1,
            default="U")

    # Admin fields
    notes_from_admin = models.TextField(
            null=True,
            blank=True)

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.draft_url)
