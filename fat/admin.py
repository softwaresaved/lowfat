from django.contrib import admin
from .models import *

class ClaimedAdmin(admin.ModelAdmin):
    list_display = [
        'surname',
        'forenames',
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
        'selected',
        'application_year',
        'gender',
    ]


class FundAdmin(admin.ModelAdmin):
    list_display = [
        'claimed',
        'name',
    ]
    search_fields = [
        'claimed__surname',
        'claimed__forenames',
        'name',
        'country',
        'city',
    ]
    list_filter = [
        'category',
        'ad_status',
        'status',
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
        if self.value() == '0':
            return queryset.filter(amount_claimed__lte=0)
        if self.value() == '1':
            return queryset.filter(amount_claimed__gt=0)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        'fund',
        'get_claimed',
        'get_start_date',
        'status',
    ]
    search_fields = [
        'fund__claimed__surname',
        'fund__claimed__forenames',
        'fund__name',
    ]
    list_filter = [
        'status',
        AmountListFilter,
    ]

    def get_claimed(self, obj):
        return obj.fund.claimed

    get_claimed.short_description = 'claimed'
    get_claimed.admin_order_field = 'fund__claimed'

    def get_start_date(self, obj):
        return obj.fund.start_date

    get_start_date.short_description = 'Start date'
    get_start_date.admin_order_field = 'fund__start_date'


class BlogAdmin(admin.ModelAdmin):
    pass

class FundSentMailAdmin(admin.ModelAdmin):
    pass


class ExpenseSentMailAdmin(admin.ModelAdmin):
    pass


class BlogSentMailAdmin(admin.ModelAdmin):
    pass


PUBLIC_MODELS = (
        (Claimed, ClaimedAdmin),
        (Fund, FundAdmin),
        (Expense, ExpenseAdmin),
        (Blog, BlogAdmin),
        (FundSentMail, FundSentMailAdmin),
        (ExpenseSentMail, ExpenseSentMailAdmin),
        (BlogSentMail, BlogSentMailAdmin),
        )


for public_model in PUBLIC_MODELS:
    admin.site.register(*public_model)
