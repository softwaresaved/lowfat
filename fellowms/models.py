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
        ('U', 'Unprocessed'),
        ('V', 'Visible'),
        ('H', 'Hide'),
        ('A', 'Archived'),
        )

EVENT_STATUS = (
        ('U', 'Unprocessed'),
        ('P', 'Processing'),
        ('A', 'Approved'),
        ('R', 'Reproved'),
        )

EXPENSE_STATUS = (
        ('W', 'Not submitted yet'),
        ('S', 'Submitted (but not processed yet)'),
        ('P', 'Processing'),
        ('A', 'Approved (waiting reply from finances)'),
        ('F', 'Finished'),
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
        unique_together = ('forenames', 'surname')

    # Authentication
    #
    # We use this to only allow fellow to access their own data.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            null=True,
            blank=True)

    # Personal info
    forenames = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    surname = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    email = models.EmailField(
            blank=False,
            unique=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGTH,
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
            null=False,
            blank=False)  # This need to be a JPG.

    # Professional info
    # JACS code for research_area.
    # https://www.hesa.ac.uk/jacs/
    research_area = models.CharField(max_length=4,
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
    inauguration_year = models.IntegerField(
            null=True,
            blank=True)
    fellowship_grant = models.IntegerField(
            default=0,
            null=False,
            blank=False)
    # Mentors need to be another fellow
    mentor = models.ForeignKey('self',
            blank=True,
            null=True)

    def __str__(self):
        return "{} {}".format(self.forenames, self.surname)

    def fellowship_available(self):
        """Return the remain fellowship grant."""
        this_fellow_events = Event.objects.filter(fellow=self)
        return self.fellowship_grant - sum([event.approve for event in this_fellow_events])


class Event(models.Model):
    """Describe a event from one fellow."""
    class Meta:
        app_label = 'fellowms'

    fellow = models.ForeignKey('Fellow',
            null=False,
            blank=False)
    category = models.CharField(choices=EVENT_CATEGORY,
            max_length=1,
            default="O")
    name = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    url = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    location = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=False)
    lon = models.FloatField(
            null=True,
            blank=True)
    lat = models.FloatField(
            null=True,
            blank=True)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    budget_request_travel = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_request_attendance_fees = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_request_subsistence_cost = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_request_venue_hire = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_request_catering = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_request_others = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    budget_approve = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    justification = models.TextField(blank=False)
    additional_info = models.TextField(blank=True)

    # Admin fields
    ad_status = models.CharField(choices=AD_STATUS,
            max_length=1,
            default="U")
    status = models.CharField(choices=EVENT_STATUS,
            max_length=1,
            default="U")
    report_url = models.CharField(max_length=MAX_CHAR_LENGTH,
            blank=True,
            null=True)

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
            null=False,
            blank=False)  # This need to be a PDF.

    # Admin fields
    status = models.CharField(choices=EXPENSE_STATUS,
            max_length=1,
            default="P")

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

    def __str__(self):
        return "{}".format(self.draft_url)
