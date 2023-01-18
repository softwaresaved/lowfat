from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models

from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ExportMixin

# This removes the user registration for the User model.
# This is only necessary because we don't have a custom user model.
# We want a required email in the user creation form, we have to patch it in the following way.
admin.site.unregister(User)


# This re registers the User model to the admin panel
# We define the email form in the fieldsets.
@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # We need to make the email EmailField a required field, it isn't by default.
    # We create a quick custom class deprecating the original email replacing it with
    # a required email field.
    class MyUserCreationForm(UserCreationForm):
        email = forms.EmailField(required=True)

    # Deprecate the add_form from UserAdmin with the custom MyUserCreationForm
    add_form = MyUserCreationForm


@admin.register(models.FundActivity)
class FundActivityAdmin(SimpleHistoryAdmin):
    pass


# Add ability to export claimant data
class ClaimantResource(resources.ModelResource):
    class Meta:
        model = models.Claimant


@admin.register(models.Claimant)
class ClaimantAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_classes = [ClaimantResource]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "forenames",
                    "surname",
                    "email",
                ]
            },
        ),
        (
            "Personal Information",
            {
                "fields": [
                    "phone",
                    "gender",
                    "home_country",
                    "home_city",
                    "home_lon",
                    "home_lat",
                    "photo",
                ]
            },
        ),
        (
            "Professional information",
            {
                "fields": [
                    "career_stage_when_apply",
                    "job_title_when_apply",
                    "research_area",
                    "research_area_code",
                    "affiliation",
                    "department",
                    "group",
                    "funding",
                    "funding_notes",
                ],
            },
        ),
        (
            "Social Media",
            {
                "fields": [
                    "institutional_website",
                    "website",
                    "website_feed",
                    "orcid",
                    "google_scholar",
                    "github",
                    "gitlab",
                    "bitbucket",
                    "twitter",
                    "linkedin",
                    "facebook",
                ]
            },
        ),
        (
            "Website",
            {
                "fields": [
                    "interests",
                    "work_description",
                    "photo_work_description",
                ]
            },
        ),
        (
            "Administration",
            {
                "fields": [
                    "slug",
                    "terms_and_conditions",
                    "application_year",
                    "inauguration_grant_expiration",
                    "shortlisted",
                    "received_offer",
                    "fellow",
                    "collaborator",
                    "is_into_training",
                    "carpentries_instructor",
                    "research_software_engineer",
                    "claimantship_grant",
                    "attended_inaugural_meeting",
                    "attended_collaborations_workshop",
                    "notes_from_admin",
                ],
            },
        ),
    ]
    list_display = [
        'forenames',
        'surname',
        'email',
        'application_year',
    ]
    search_fields = [
        'surname',
        'forenames',
        'email',
        'home_country',
        'home_city',
        'research_area',
        'research_area_code',
        'affiliation',
        'funding',
        'funding_notes',
        'work_description'
    ]
    list_filter = [
        'fellow',
        'collaborator',
        'received_offer',
        'application_year',
        'gender',
        'career_stage_when_apply',
        'research_area_code',
        'is_into_training',
        'carpentries_instructor',
        'research_software_engineer',
    ]


@admin.register(models.Fund)
class FundAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'claimant',
                'title',
                'url',
                'country',
                'city',
                'lon',
                'lat',
                'start_date',
                'end_date',
                'justification',
                'additional_info',
                'extra_sponsored',
            ]
        }),
        ('Budget', {
            'fields': [
                'budget_request_travel',
                'budget_request_attendance_fees',
                'budget_request_subsistence_cost',
                'budget_request_venue_hire',
                'budget_request_catering',
                'budget_request_others',
                'budget_approved',
            ]
        }),
        ('Success', {
            'fields': [
                'success_targeted',
                'success_reported',
            ]
        }),
        ('Metadata', {
            'fields': [
                'category',
                'focus',
                'activity',
                'mandatory',
                'direct_invoice'
            ]
        }),
        ('Publicity', {
            'fields': [
                'can_be_included_in_calendar',
                'can_be_advertise_before',
                'can_be_advertise_after',
            ]
        }),
        ('Admin', {
            'fields': [
                'ad_status',
                'status',
                'required_blog_posts',
                'grant',
                'grant_heading',
                'notes_from_admin',
                'access_token',
            ]
        }),
    ]
    list_display = [
        'claimant',
        'title',
        'added',
    ]
    search_fields = [
        'claimant__surname',
        'claimant__forenames',
        'title',
        'country',
        'city',
    ]
    list_filter = [
        'category',
        'ad_status',
        'status',
        'grant',
        'grant_heading',
        'focus',
        'mandatory',
        'direct_invoice',
        'activity',
    ]


class AmountListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'amount'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'amount_claimed'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', '£0'),
            ('1', '> £0'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        query = None
        if self.value() == '0':
            query = queryset.filter(amount_claimed__lte=0)
        if self.value() == '1':
            query = queryset.filter(amount_claimed__gt=0)

        return query


@admin.register(models.Expense)
class ExpenseAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'fund',
                'claim',
                'receipts',
                'supporting_docs',
                'amount_claimed',
                'justification_for_extra',
                'final',
            ]
        }),
        ('Requests', {
            'fields': [
                'invoice',
                'invoice_reference',
                'advance_booking',
            ]
        }),
        ('Recipient', {
            'fields': [
                'recipient_fullname',
                'recipient_email',
                'recipient_affiliation',
                'recipient_group',
                'recipient_connection',
            ]
        }),
        ('Admin', {
            'fields': [
                'status',
                'amount_authorized_for_payment',
                'asked_for_authorization_date',
                'send_to_finance_date',
                'grant_heading',
                'grant',
                'upload_final_claim_form',
                'notes_from_admin',
            ]
        })
    ]
    list_display = [
        'fund',
        'get_claimant',
        'get_start_date',
        'status',
        'invoice',
        'advance_booking',
    ]
    search_fields = [
        'fund__claimant__surname',
        'fund__claimant__forenames',
        'fund__title',
    ]
    list_filter = [
        'status',
        'invoice',
        'advance_booking',
        AmountListFilter,
    ]

    def get_claimant(self, obj):  # pylint: disable=no-self-use
        return obj.fund.claimant

    get_claimant.short_description = 'claimant'
    get_claimant.admin_order_field = 'fund__claimant'

    def get_start_date(self, obj):  # pylint: disable=no-self-use
        return obj.fund.start_date

    get_start_date.short_description = 'Start date'
    get_start_date.admin_order_field = 'fund__start_date'


@admin.register(models.Blog)
class BlogAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'author',
                'coauthor',
                'fund',
                'draft_url',
                'final',
                'notes_from_author',
            ]
        }),
        ('Publish information', {
            'fields': [
                'status',
                'title',
                'published_url',
                'tweet_url',
            ]
        }),
        ('Admin', {
            'fields': [
                'reviewer',
                'notes_from_admin',
            ]
        })
    ]
    list_display = [
        'author',
        'fund',
        'added',
    ]
    search_fields = [
        'fund',
        'author',
        'coauthor',
        'notes_from_author',
        'notes_from_admin',
        'title',
        'published_url',
        'tweet_url',
    ]
    list_filter = [
        'status',
    ]


@admin.register(models.FundSentMail)
class FundSentMailAdmin(SimpleHistoryAdmin):
    pass


@admin.register(models.ExpenseSentMail)
class ExpenseSentMailAdmin(SimpleHistoryAdmin):
    pass


@admin.register(models.BlogSentMail)
class BlogSentMailAdmin(SimpleHistoryAdmin):
    pass


@admin.register(models.TermsAndConditions)
class TermsAndConditionsAdmin(SimpleHistoryAdmin):
    pass
