import datetime

import pandas as pd

from django.contrib.auth.models import User, BaseUserManager
from django.core.management.base import BaseCommand

from lowfat.models import Expense

class Command(BaseCommand):
    help = "Change claims date to last day of fellowship."

    def handle(self, *args, **options):
        for expense in Expense.objects.all():
            if expense.received_date == datetime.date(1, 1, 1):  # This is possible because of our import script
                print("Changing dates for {}".format(expense))
                expense.received_date = expense.fund.claimant.inauguration_grant_expiration
                expense.added = datetime.datetime(
                    expense.fund.claimant.inauguration_grant_expiration.year,
                    expense.fund.claimant.inauguration_grant_expiration.month,
                    expense.fund.claimant.inauguration_grant_expiration.day
                )
                expense.save()
