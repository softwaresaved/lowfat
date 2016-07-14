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
