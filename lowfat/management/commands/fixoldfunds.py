import datetime

import pandas as pd

from django.contrib.auth.models import User, BaseUserManager
from django.core.management.base import BaseCommand

from lowfat.models import Fund, Expense

class Command(BaseCommand):
    help = "Change funding requests and expenses claims dates imported with loadoldfunds.py to last day of fellowship."

    def handle(self, *args, **options):
        for fund in Fund.objects.all():
            day = datetime.timedelta(1)
            if fund.added - datetime.datetime(2016, 12, 22) < day:  # This is the day that we ran import script
                print("Changing dates for {}".format(fund))
                if fund.end_date < fund.claimant.inauguration_grant_expiration:
                    # This is part of their fellowship
                    fund.added = datetime.datetime(
                        fund.claimant.application_year + 1,
                        1,
                        1
                    )
                else:
                    fund.added = datetime.datetime(
                        fund.start_date.year,
                        fund.start_date.month,
                        1
                    ) - datetime.timedelta(30)
                fund.save()

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
