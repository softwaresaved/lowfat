from datetime import date, timedelta
import re
import uuid

import django.utils
from django.conf import settings
from django.db import models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from lowfat.validator import online_document

BLOG_POST_STATUS = (
    ('U', 'Waiting for triage'),  # This is the status after we receive the blog post draft.
    ('R', 'Waiting to be reviewed'),  # Blog post is assigned to one staff to be reviewed.
    ('C', 'Reviewing loop'),  # Blog post is waiting for another reviewing interaction.
    ('G', 'Waiting to be proofread'),  # Blog post is assigned to be proofread by the community officer.
#    ('L', 'Waiting to be published'),  # Blog post will be published by the community officer.
    ('P', 'Published'),  # Blog post is published and have a URL at the website.
#   ('M', 'Mistaked'),  # Blog post submitted by mistake.
    ('K', 'Cancelled'), # New blog post status inline with fund and expense claim model status.
    ('D', 'Rejected'),  # Blog post is rejected for any reason.
#    ('O', 'Out of date'),  # Blog post that wait too long to be published for any reason.
    ('X', 'Removed'),  # When the fellow decided to remove their request...Update: Changed Remove--->Removed to be consistent with fund & expense statuses
)

MAX_CHAR_LENGTH = 120
MAX_URL_LENGTH = 360


def fix_url(url):
    """Prepend 'http://' to URL."""
    if url is not None and url:
        url = url.split()[0]  # If the URL uses white space it should be encoded as %20%
        url = url.split(",")[0]  # If the URL uses comma it should be encoded as %2C.
        if not re.match("https?://", url):
            url = "http://{}".format(url)

    return url


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


class Blog(ModelWithToken):
    """Provide the link to the blog post about the fund."""
    class Meta:
        app_label = 'lowfat'
        ordering = [
            "-added",
        ]

    # Form
    fund = models.ForeignKey(
        'Fund',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'Claimant',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    coauthor = models.ManyToManyField(
        'Claimant',
        blank=True,
        related_name="author"
    )
    draft_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        validators=[online_document]
    )
    final = models.BooleanField(
        default=False
    )
    notes_from_author = models.TextField(
        null=True,
        blank=True
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
        blank=True,
        on_delete=models.CASCADE
    )
    notes_from_admin = models.TextField(
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        null=True,
        blank=True
    )
    published_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        null=True,
        blank=True
    )
    tweet_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        null=True,
        blank=True
    )

    # Control
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def remove(self):
        self.status = "X"
        self.save()

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        self.draft_url = fix_url(self.draft_url)
        self.published_url = fix_url(self.published_url)
        self.tweet_url = fix_url(self.tweet_url)

        if self.published_url:
            self.status = 'P'
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.draft_url)

    def link(self):
        if self.access_token:
            link = reverse("blog_detail_public", args=[self.access_token])
        else:
            link = reverse("blog_detail", args=[self.id])
        return link

    def link_review(self):
        return reverse("blog_review", args=[self.id])


class GeneralSentMail(models.Model):
    """Emails sent with custom text."""
    class Meta:
        app_label = 'lowfat'
        ordering = [
            "date",
        ]

    justification = models.TextField()

    # Internal
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,  # For confirmation email
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey('Claimant', on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)
    history = HistoricalRecords()


class FundSentMail(GeneralSentMail):
    fund = models.ForeignKey('Fund', on_delete=models.CASCADE)


class ExpenseSentMail(GeneralSentMail):
    expense = models.ForeignKey('Expense', on_delete=models.CASCADE)


class BlogSentMail(GeneralSentMail):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
