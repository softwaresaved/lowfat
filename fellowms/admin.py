from django.contrib import admin
from .models import Collaborator, Fellow, Event, Expense, Blog

PUBLIC_MODELS = (
        Collaborator,
        Fellow,
        Event,
        Expense,
        Blog
        )

for public_model in PUBLIC_MODELS:
    admin.site.register(public_model)
