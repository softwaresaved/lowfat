from django.contrib import admin
from .models import Fellow, Event, Expense, Blog

class FellowAdmin(admin.ModelAdmin):
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
        'home_location',
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


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'fellow',
        'name',
    ]
    search_fields = [
        'fellow__surname',
        'fellow__forenames',
        'name',
        'location',
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
        'event',
        'status',
    ]
    search_fields = [
        'event__fellow__surname',
        'event__fellow__forenames',
        'event__name',
    ]
    list_filter = [
        'status',
        AmountListFilter,
    ]


class BlogAdmin(admin.ModelAdmin):
    pass


PUBLIC_MODELS = (
        (Fellow, FellowAdmin),
        (Event, EventAdmin),
        (Expense, ExpenseAdmin),
        (Blog, BlogAdmin),
        )


for public_model in PUBLIC_MODELS:
    admin.site.register(*public_model)
