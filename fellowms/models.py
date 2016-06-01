import uuid

from django.db import models

MAX_CHAR_LENGHT = 120
MAX_PHONE_LENGHT = 14
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

EVENT_STATUS = (
        ('U', 'Unprocessed'),
        ('P', 'Processing'),
        ('A', 'Approved'),
        ('R', 'Reproved'),
        )

EXPENSE_STATUS = (
        ('P', 'Processing'),
        ('F', 'Finished'),
        )

class Fellow(models.Model):
    """Describe a fellow."""
    class Meta:
        app_label = 'fellowms'

    # Personal info
    forenames = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    surname = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    email = models.EmailField(
            blank=False,
            unique=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGHT,
            blank=False,
            unique=True)
    gender = models.CharField(choices=GENDERS,
            max_length=1,
            default="R")
    home_location = models.CharField(max_length=MAX_CHAR_LENGHT,
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
    affiliation = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    funding = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    funding_notes = models.TextField(
            null=True,
            blank=True)
    work_description = models.TextField(blank=False)

    # Social media
    website = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    website_feed = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    orcid = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    github = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    gitlab = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    twitter = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)
    facebook = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=True)

    # Admin fields
    inauguration_year = models.IntegerField(blank=False,
            default=2017)
    # Mentors need to be another fellow
    mentor = models.ForeignKey('self',
            blank=True,
            null=True)

    def __str__(self):
        return "{} {}".format(self.forenames, self.surname)


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
    name = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    url = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    location = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
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
    status = models.CharField(choices=EVENT_STATUS,
            max_length=1,
            default="U")

    def __str__(self):
        return "{}".format(self.name)


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
        return self.proof


class Blog(models.Model):
    """Provide the link to the blog post about the event."""
    class Meta:
        app_label = 'fellowms'

    event = models.ForeignKey('Event',
            null=False,
            blank=False)
    draft_url = models.CharField(max_length=MAX_CHAR_LENGHT,
                blank=False)

    def __str__(self):
        return "{}".format(self.draft_url)
