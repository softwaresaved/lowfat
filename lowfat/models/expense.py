from datetime import date, timedelta
import hashlib
from django.urls import reverse
from simple_history.models import HistoricalRecords
import uuid
from django.db import models
from lowfat.validator import pdf

EXPENSE_STATUS = (
    ('S', 'Submitted'),
    ('C', 'Processing'),
    ('A', 'Approved'),
    ('R', 'Rejected'),  # When expense was rejected.
    ('X', 'Remove'),  # When the fellow decided to remove their request.
)

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

INVOICE_HASH = hashlib.md5()
MAX_CHAR_LENGTH = 120
MAX_DIGITS = 10
MAX_INVOICE_REFERENCE_LENGTH = 14  # e.g. SSIF-xxxx-xxxx


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


class Expense(ModelWithToken):
    """This describe one expense for one fund."""
    class Meta:
        app_label = 'lowfat'
        ordering = [
            "-added",
            "relative_number",
        ]

    # Internal
    relative_number = models.IntegerField(
        null=False,
        blank=False
    )
    invoice_reference = models.CharField(
        max_length=MAX_INVOICE_REFERENCE_LENGTH,
        null=True,
        blank=True
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
        blank=True
    )
    invoice = models.BooleanField(
        default=False
    )
    final = models.BooleanField(
        default=False
    )
    advance_booking = models.BooleanField(
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
        blank=True,
        help_text="You need to provide a reason for submit the recipient claim. An common reasons is \"because the recipient was of of the speakers on that workshop.\""
    )

    # Admin fields
    status = models.CharField(
        choices=EXPENSE_STATUS,
        max_length=1,
        default="S"
    )
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
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return "Expense {} - {}".format(
            self.id,
            self.claim.name
        )

    def remove(self):
        self.status = "X"
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if self.pk is None:
            previous_expenses = Expense.objects.filter(fund=self.fund).order_by("-pk")
            if previous_expenses:
                self.relative_number = previous_expenses[0].relative_number + 1
            else:
                self.relative_number = 1

            if self.fund.mandatory:  # pylint: disable=no-member
                self.grant_heading = 'I'  # Use of Core fund
            else:
                self.grant_heading = self.fund.grant_heading  # pylint: disable=no-member
            self.grant = self.fund.grant  # pylint: disable=no-member

            if self.invoice:
                INVOICE_HASH.update(bytes("{} - {} #{}".format(
                    self.fund.claimant.fullname,  # pylint: disable=no-member
                    self.fund.title,
                    self.relative_number
                ), 'utf-8'))
                self.invoice_reference = "SSIF-{}-{}".format(
                    INVOICE_HASH.hexdigest()[0:5],
                    INVOICE_HASH.hexdigest()[5:9]
                )

        super().save(*args, **kwargs)

    def link(self):
        if self.access_token:
            link = reverse("expense_detail_public", args=[self.access_token])

        else:
            link = reverse("expense_detail_relative", args=[self.fund.id, self.relative_number])

        return link

    def link_review(self):
        return reverse("expense_review_relative", args=[self.fund.id, self.relative_number])

    def link_claim(self):
        return reverse("expense_claim_relative", args=[self.fund.id, self.relative_number])

    def claim_clean_name(self):
        return "{}".format(
            self.claim.name.replace("/", "-")
        )
