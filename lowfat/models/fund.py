from datetime import datetime, date, timedelta
import logging
import re
import uuid

from geopy.geocoders import Nominatim

from constance import config

from django.conf import settings
from django.db import models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from django_countries.fields import CountryField

import tagulous.models

from lowfat.utils import ChoicesEnum
from .blog import Blog
from .expense import Expense

logger = logging.getLogger(__name__)

AD_STATUS = (
    ('U', 'Unprocessed'),  # Initial status
    ('V', 'Visible'),  # Fund is visible on map
    ('H', 'Hide'),  # Fund is invisible on map
)

FUND_CATEGORY = (
    ('A', 'Attending'),
    ('H', 'Organising'),
)

FUND_FOCUS = (
    ('D', 'Domain specific'),
    ('C', 'Cross cutting'),
)

FUND_STATUS = (
    ('U', 'Unprocessed'),  # Initial status
    ('P', 'Processing'),  # When someone was assigned to review the request
    ('A', 'Approved'),  # Fund was approved. Funds are reserved.
    ('M', 'Approved by machine'),  # Fund was approved by machine. Funds are reserved.
    ('R', 'Rejected'),  # Fund was rejected.
    ('F', 'Archived'),  # Approved funds with all claims and blog posts were processed. No funds are reserved.
    ('C', 'Cancelled'),  # When the fellow decided to cancel their request.
    ('X', 'Removed'),  # When the fellow decided to remove their request. UPDATE: The option is only available to the admin!
)

#: Set of statuses which constitute an approved fund
FUND_STATUS_APPROVED_SET = {
    'A',
    'M',
}

FUND_STATUS_LONG_DESCRIPTION = {
    'U': "We didn't start to process your request yet.",
    'P': "One of your staffs is reviewing your request. You should have our reply soon.",
    'A': "Your fund request was approved.",
    'M': "Your fund request was pre-approved.",
    'R': "Your fund request was declined.",
    'F': "We archived your fund request since all the expense claims were processed.",
    'C': "You decided to cancel this request for any reason.",
    'X': "You decided to remove this request.",
}

GRANT_HEADING = (
    ('C', 'Continuing (claimantship)'),
    ('I', 'Core (Software Sustainability Institute)'),
    ('F', 'Grant (inauguration claimantship)'),
)

GRANTS = (
    ('SSI1', 'Software Sustainability Institute - Phase 1'),
    ('SSI2', 'Software Sustainability Institute - Phase 2'),
    ('SSI3', 'Software Sustainability Institute - Phase 3'),
    ('SSI4', 'Software Sustainability Institute - Phase 4'),
)

FUND_PAYMENT_RECEIVER_CHOICES = [
    ('A', 'A. Me (the Fellow)'),
    ('B', 'B. Third party'),
    ('C', 'C. Combination of both'),
]

FUND_CLAIM_METHOD_CHOICES = [
    ('A', 'A. Expense claim'),
    ('B', 'B. Invoice'),
    ('C', 'C. Combination of both'),
]

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


def pair_fund_with_blog(funds, status=None):  # called in views.claimant
    """Create list of tuples where first element is fund and second is list of blog related with it."""
    args = {}
    if status:
        args["status"] = status

    return [(fund, Blog.objects.filter(
        fund=fund,
        **args
    )) for fund in funds]


class FundActivity(tagulous.models.TagTreeModel):  # pylint: disable=model-no-explicit-unicode
    class Meta:
        verbose_name = 'Fund Activity Tag'
        verbose_name_plural = 'Fund Activity Tags'
        ordering = [
            "name",
        ]

    class TagMeta:
        initial = "attending as ssi, conference, field trip, focus group, hack, knowledge exchange, local, meeting, " \
                  "new paradigm, new resource, organising submeeting, panel, paying for others, policy, " \
                  "poster presentation, prize, roundtable, roundtable/lead, software Special Interest Group, " \
                  "ssi organised, supported collaborator, survey, talk at, talk at/invited, teaching at, " \
                  "teaching as helper, training/attending, training/organiser, unconference, working group, workshop"
        force_lowercase = True
        autocomplete_view = None
        protected = True
        space_delimiter = False


class ApprovalChain(ChoicesEnum):
    """
    Which approval chain is required to authorise this request?
    """
    FELLOWS = "fellows"
    ONE_TIME = "onetime"

    @classmethod
    def email_address(cls, chain):
        if chain == cls.FELLOWS:
            return config.FELLOWS_MANAGEMENT_EMAIL

        if chain == cls.ONE_TIME:
            return config.ONETIME_APPROVAL_EMAIL

        raise ValueError("Approval chain has not been fully defined")


class ModelWithToken(models.Model):
    class Meta:
        abstract = True

    # Access token
    access_token = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    access_token_expire_date = models.DateField(
        null=True,
        blank=True
    )

    def new_access_token(self):
        self.access_token = uuid.uuid4().hex
        self.access_token_expire_date = date.today() + timedelta(days=30)
        self.save()

    def access_token_is_valid(self):
        if self.access_token_expire_date is not None:
            return date.today() < self.access_token_expire_date
        return False


class Fund(ModelWithToken):
    """Describe a fund from one claimant."""
    class Meta:
        app_label = 'lowfat'
        ordering = [
            "-start_date",
            "-end_date",
            "title",
        ]

    # TODO Make claimant more generic to include staffs.
    claimant = models.ForeignKey('Claimant', on_delete=models.CASCADE)
    category = models.CharField(
        choices=FUND_CATEGORY,
        max_length=1,
        default="A"
    )
    focus = models.CharField(
        choices=FUND_FOCUS,
        max_length=1,
        default="C"
    )
    activity = tagulous.models.TagField(
        to=FundActivity,
        blank=True
    )
    mandatory = models.BooleanField(default=False)
    title = models.CharField(max_length=MAX_CHAR_LENGTH)
    url = models.CharField(
        max_length=MAX_URL_LENGTH,
        blank=True,  # See https://github.com/softwaresaved/lowfat/issues/192
    )
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
    #direct_invoice = models.BooleanField(default=False)
    fund_payment_receiver = models.CharField(
        max_length=1,
        choices=FUND_PAYMENT_RECEIVER_CHOICES,
        null=True,
        blank=True,
    )
    fund_claim_method = models.CharField(
        max_length=1,
        choices=FUND_CLAIM_METHOD_CHOICES,
        null=True,
        blank=True,
    )
    justification = models.TextField()
    success_targeted = models.TextField()
    success_reported = models.TextField(blank=True)  # Only provide later
    additional_info = models.TextField(blank=True)
    extra_sponsored = models.TextField(blank=True)

    # Publicity
    can_be_included_in_calendar = models.BooleanField(default=False)  # For privacy.
    can_be_advertise_before = models.BooleanField(default=False)  # For privacy.
    can_be_advertise_after = models.BooleanField(default=True)  # For fulfilment of contract.

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
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    required_blog_posts = models.IntegerField(
        null=False,
        blank=True
    )
    grant_heading = models.CharField(
        choices=GRANT_HEADING,
        max_length=1,
        default="F"
    )
    grant = models.CharField(
        choices=GRANTS,
        max_length=4,
        default="SSI3"
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    approved = models.DateTimeField(
        null=True,
        blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    #: Who is required to approve this request?
    approval_chain = models.CharField(
        choices=ApprovalChain.choices(),
        max_length=8,
        default=ApprovalChain.FELLOWS
    )

    def remove(self):
        self.status = "X"
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if not self.pk:
            self.grant = config.GRANTS_DEFAULT
            if date.today() < self.claimant.inauguration_grant_expiration:  # pylint: disable=no-member
                self.grant_heading = "F"
            else:
                self.grant_heading = "C"

        if self.status in FUND_STATUS_APPROVED_SET:
            self.approved = datetime.now()

        if self.required_blog_posts is None:
            # Blog posts are not required if an event is mandatory - e.g. collaborations workshop
            self.required_blog_posts = 0 if self.mandatory else 1

        self.url = fix_url(self.url)

        super().save(*args, **kwargs)

    def update_latlon(self):
        geolocator = Nominatim(user_agent="lowfat/dev")

        try:
            location = geolocator.geocode(
                self.city,
                country_codes=[self.country.code]
            )

            if location is not None:
                self.lon = location.longitude
                self.lat = location.latitude

                self.save()

        except Exception as exc:  # pylint: disable=broad-except
            logger.error(exc, exc_info=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.id)

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
        """Return the total amount of expenses claimant."""
        this_fund_expenses = Expense.objects.filter(
            fund=self,
            status__in=["S", "C", "A", "M"]
        )
        return sum([expense.amount_claimed for expense in this_fund_expenses])

    def expenses_claimed_left(self):
        """Return the total amount left to claimant."""
        return self.budget_total() - self.expenses_claimed()

    def expenses_authorized_for_payment(self):
        """Return the total amount of expenses authorized_for_payment."""
        this_fund_expenses = Expense.objects.filter(
            fund=self,
            status__in=FUND_STATUS_APPROVED_SET
        )
        return sum([expense.amount_authorized_for_payment for expense in this_fund_expenses])

    def total_of_blog_posts(self):
        """Return number of blog posts."""
        return Blog.objects.filter(fund=self).count()

    def link(self):
        if self.access_token:
            link = reverse("fund_detail_public", args=[self.access_token])
        else:
            link = reverse("fund_detail", args=[self.id])
        return link

    def title_link(self):
        return """<a href="{}">{}</a>""".format(
            self.link(),
            self.title
        )

    def link_review(self):
        return reverse("fund_review", args=[self.id])

    def pre_approve(self):
        approved = False

        if self.mandatory and self.budget_total() < config.PRE_APPROVED_FUNDING_REQUEST_BUDGET:
            self.status = 'M'
            self.save()
            approved = True

        return approved

    def new_access_token(self):
        self.access_token = uuid.uuid4().hex
        today = date.today()
        if today < self.end_date:
            self.access_token_expire_date = self.end_date + timedelta(days=30)
        else:
            self.access_token_expire_date = today + timedelta(days=30)
        self.save()
