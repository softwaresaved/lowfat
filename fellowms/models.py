from django.db import models

MAX_CHAR_LENGHT = 120
MAX_PHONE_LENGHT = 14
MAX_DIGITS = 10

GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('R', 'Rather not say'),
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

    forenames = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    surname = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    affiliation = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    # JACS code for research_area.
    # https://www.hesa.ac.uk/jacs/
    research_area = models.CharField(max_length=4,
            blank=False,
            unique=True)
    email = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGHT,
            blank=False,
            unique=True)
    gender = models.CharField(choices=GENDER,
            max_length=1,
            default="R")
    work_description = models.TextField(blank=False)
    year = models.IntegerField(blank=False,
            default=2017)

    def __str__(self):
        return "{} <{}>".format(self.full_name, self.email)


class Event(models.Model):
    """Describe a event from one fellow."""
    class Meta:
        app_label = 'fellowms'

    fellow = models.ForeignKey('Fellow',
            null=False,
            blank=False)
    url = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    name = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    description = models.TextField(blank=False)
    budget_request = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False)
    budget_approve = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False,
            default=0.00)
    status = models.CharField(choices=EVENT_STATUS,
            max_length=1,
            default="U")

    def __str__(self):
        return "{}".format(self.name)


class Expense(models.Model):
    """This describe one expense for one event."""
    class Meta:
        app_label = 'fellowms'

    proof = models.FileField(
            upload_to='expenses/',  # File will be uploaded to MEDIA_ROOT/expenses
            null=False,
            blank=False)  # This need to be a PDF.
    event = models.ForeignKey('Event',
            null=False,
            blank=False)
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
