import pandas as pd

from django.contrib.auth.models import User, BaseUserManager
from django.core.management.base import BaseCommand

from lowfat.models import Expense

class Command(BaseCommand):
    help = "Review claims looking for wrong date."

    def handle(self, *args, **options):
        for expense in Expense.objects.all():
            if expense.funds_from != "F" and expense.received_date > expense.fund.claimant.inauguration_grant_expiration:
                expense.received_date = expense.fund.claimant.inauguration_grant_expiration
                expense.save()
