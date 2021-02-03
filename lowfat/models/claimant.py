from datetime import date
import itertools
import re

from geopy.geocoders import Nominatim

from constance import config

from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

import django.utils.text
from django.conf import settings
from django.db import models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from django_countries.fields import CountryField

from lowfat.jacs import JACS_3_0_PRINCIPAL_SUBJECT_CODES
from .fund import Fund, FUND_STATUS_APPROVED_SET
from .expense import Expense

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('R', 'Rather not say'),
)

CAREER_STAGES = (
    ('1', 'Phase 1 - Junior (e.g. PhD candidate, Junior Research Software Engineer)'),
    ('2', 'Early (e.g Research Assistant/Associate, first grant holder, Lecturer, Research Software Engineer)'),
    ('3', 'Mid / Recognised (e.g. Senior Lecturer, Reader, Senior Researcher, Senior Research Software Engineer, Research Software Group Leader)'),
    ('4', 'Established / Experienced / Senior  (e.g. Professor, Director of Research Computing, Distinguished Engineer, Chief Data Scientist)'),
)

MAX_CHAR_LENGTH = 120
MAX_DIGITS = 10
MAX_URL_LENGTH = 360


def fix_url(url):
    """Prepend 'http://' to URL."""
    if url is not None and url:
        url = url.split()[0]  # If the URL uses white space it should be encoded as %20%
        url = url.split(",")[0]  # If the URL uses comma it should be encoded as %2C.
        if not re.match("https?://", url):
            url = "http://{}".format(url)

    return url


class TermsAndConditions(models.Model):
    """Terms and Conditions information."""
    class Meta:
        ordering = [
            "-year",
        ]
        verbose_name_plural = "terms and conditions"

    #: Programme year for which this terms and conditions page is valid
    year = models.CharField(  # Year as string so it can be used for special cases.
        max_length=4,  # YYYY
        primary_key=True
    )

    #: URL of terms and conditions page
    url = models.CharField(  # External web page.
        max_length=MAX_CHAR_LENGTH
    )

    def __str__(self):
        return "{} Terms & Conditions".format(
            self.year
        )


class Claimant(models.Model):
    """Describe a claimant."""

    class Meta:
        app_label = 'lowfat'
        ordering = [
            "-fellow",
            "-application_year",
            "forenames",
            "surname",
        ]

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
        blank=True,  # This need to be a JPG.
        help_text="A professionally oriented (i.e. work related) thumbnail picture of yourself that you are"
                  " happy to be published on the web - this should be 150px wide and 150px high (exact please)."
    )
    photo_thumb = ImageSpecField(
        source='photo',
        processors=[Thumbnail(width=150, height=150, upscale=True)]
    )

    # Professional info
    career_stage_when_apply = models.CharField(
        choices=CAREER_STAGES,
        max_length=1,
        default="M"
    )
    job_title_when_apply = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    research_area = models.TextField(
        blank=True,
        help_text="Please describe your research"
    )
    # JACS code for research_area.
    # https://www.hesa.ac.uk/jacs/
    research_area_code = models.CharField(
        choices=JACS_3_0_PRINCIPAL_SUBJECT_CODES,
        max_length=2,
        default="Y0"
    )
    affiliation = models.CharField(  # Home institution
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    department = models.CharField(  # Department within home institution
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    group = models.CharField(  # Group within department
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

    # Website
    #
    # See https://www.software.ac.uk/fellows/
    interests = models.TextField(
        blank=True,
        help_text="25-50 word summary of your professional interests."
    )
    work_description = models.TextField(
        blank=True,
        help_text="200-300 words describing the work you do, this can include your plans for Fellowship."
    )
    photo_work_description = models.FileField(
        upload_to='photos/',  # File will be uploaded to MEDIA_ROOT/photos
        null=True,
        blank=True,  # This need to be a JPG.
        help_text="A professionally oriented (i.e. work related) main picture of yourself that you are happy to be published on the web - this should be 300px wide and 400px high (exact please)."
    )
    photo_work_thumb = ImageSpecField(
        source='photo_work_description',
        processors=[Thumbnail(width=150, height=150, upscale=True)]
    )

    # Social media
    institutional_website = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True
    )
    website = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True
    )
    website_feed = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True
    )
    orcid = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    google_scholar = models.CharField(  # For example, https://scholar.google.co.uk/citations?user=XXXXXXXXXXXX
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
    bitbucket = models.CharField(  # https://bitbucket.org/
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    twitter = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    linkedin = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )
    facebook = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True
    )

    # Admin fields
    slug = models.CharField(max_length=MAX_CHAR_LENGTH)
    terms_and_conditions = models.ForeignKey(
        'TermsAndConditions',
        null=True,
    )
    application_year = models.IntegerField(
        null=False,
        blank=False,
        default=date.today().year
    )
    inauguration_grant_expiration = models.DateField(
        null=False,
        blank=False,
        default=date(  # This will be overwrite by save().
            date.today().year + 2,
            3,
            31
        )
    )
    shortlisted = models.BooleanField(default=False)
    received_offer = models.BooleanField(default=False)
    fellow = models.BooleanField(default=False)
    collaborator = models.BooleanField(default=False)
    is_into_training = models.BooleanField(default=False)
    carpentries_instructor = models.BooleanField(default=False)
    research_software_engineer = models.BooleanField(default=False)
    claimantship_grant = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=2,
        null=False,
        blank=False,
        default=0.00
    )
    attended_inaugural_meeting = models.BooleanField(default=False)
    attended_collaborations_workshop = models.BooleanField(default=False)  # pylint: disable=invalid-name
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )

    # Application
    screencast_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True,  # See https://github.com/softwaresaved/lowfat/issues/192
    )
    example_of_writing_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True,  # See https://github.com/softwaresaved/lowfat/issues/192
    )

    # Mentors need to be another claimant
    mentor = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('claimant-slug-resolution', kwargs={'claimant_slug': self.slug})

    def slug_generator(self):
        """
        Generate slug for Claimant - checking that it doesn't conflict with an existing Claimant.
        """
        base_slug = django.utils.text.slugify("{0}-{1}".format(self.forenames, self.surname))
        slug = base_slug

        for i in itertools.count():
            try:
                # Has this slug already been used?
                existing = Claimant.objects.get(slug=slug)
                if existing.pk == self.pk:
                    break

            except Claimant.DoesNotExist:
                # No - use this slug
                break

            except Claimant.MultipleObjectsReturned:
                # Yes - multiple times - try the next one
                pass

            # Yes - try the next one
            slug = '{0}-{1}'.format(base_slug, i)

        return slug

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if not self.id:
            self.inauguration_grant_expiration = date(
                date.today().year + 2,
                config.FELLOWSHIP_EXPENSES_END_MONTH,
                config.FELLOWSHIP_EXPENSES_END_DAY
            )

        if not self.slug:
            self.slug = self.slug_generator()

        self.website = fix_url(self.website)
        self.website_feed = fix_url(self.website_feed)

        super().save(*args, **kwargs)

    def update_latlon(self):
        geolocator = Nominatim(
            country_bias=self.home_country,
            user_agent="lowfat/dev"
        )
        try:
            location = geolocator.geocode(
                self.home_city
            )
            if location is not None:
                self.home_lon = location.longitude
                self.home_lat = location.latitude

                self.save()
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)

    def __str__(self):
        return "{} ({}{})".format(
            self.fullname(),
            self.application_year + 1,
            " ✓" if self.fellow else ""
        )

    def fullname(self):
        return "{} {}".format(self.forenames, self.surname)

    def link(self):
        if self.fellow:
            function_name = "fellow_slug"
        else:
            function_name = "claimant_slug"
        return reverse(function_name, args=[self.slug])

    def fullname_link(self):
        return """<a href="{}">{} {}</a>""".format(
            self.link(),
            self.forenames,
            self.surname
        )

    def claimantship_available(self):
        """Return the remaining claimantship grant."""
        money_available = 0
        if self.inauguration_grant_expiration > date.today():
            money_available = self.claimantship_grant - self.claimantship_committed() - self.claimantship_spent()

        return money_available

    def claimantship_passed(self):
        """Return the amount already spent from the claimantship grant."""
        money_passed = 0
        if self.inauguration_grant_expiration < date.today():
            money_passed = self.claimantship_grant - self.claimantship_committed() - self.claimantship_spent()

        return money_passed

    def claimantship_committed(self):
        """Return the amount committed from the claimantship grant."""
        this_claimant_funds = Fund.objects.filter(
            claimant=self,
            status__in=FUND_STATUS_APPROVED_SET,
            grant_heading="F"
        )

        spent_from_committed = 0
        for fund in this_claimant_funds:
            spent_from_committed += sum([expense.amount_claimed for expense in Expense.objects.filter(
                fund=fund,
                status__in=['A', 'M', 'F']
            )])

        return sum([fund.budget_approved for fund in this_claimant_funds]) - spent_from_committed

    def claimantship_spent(self):
        """Return the amount already spent from the claimantship grant."""
        this_claimant_expenses = Expense.objects.filter(
            fund__claimant=self,
            status__in=['A', 'M', 'F'],
            grant_heading="F"
        )

        return sum([expense.amount_claimed for expense in this_claimant_expenses])
