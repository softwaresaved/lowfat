from django.contrib import admin
from .models import Fellow, Event, Expense, Blog

PUBLIC_MODELS = (
        Fellow,
        Event,
        Expense,
        Blog
        )

for public_model in PUBLIC_MODELS:
    admin.site.register(public_model)
