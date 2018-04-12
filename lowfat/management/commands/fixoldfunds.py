# WARNING Commit 441fc27 will break this script

import datetime

from django.core.management.base import BaseCommand

from lowfat.models import Fund, Expense

class Command(BaseCommand):
    help = "Change funding requests and expenses claims dates imported with loadoldfunds.py to last day of fellowship."

    def handle(self, *args, **options):
        for fund in Fund.objects.all():
            day = datetime.timedelta(1)
            if fund.added - datetime.datetime(2016, 12, 22) < day:  # This is the day that we ran import script
                print("Changing dates for {}".format(fund))
                provisional_date = fund.start_date - datetime.timedelta(30)
                if fund.start_date.year == fund.claimant.application_year + 1 and provisional_date.year != fund.start_date.year:
                    # Fellow can't request the funding before their fellowship start!
                    # We will use the first day of the year
                    provisional_date = datetime.datetime(
                        fund.start_date.year,
                        1,
                        1
                    )
                fund.added = datetime.datetime(
                    provisional_date.year,
                    provisional_date.month,
                    provisional_date.day
                )
                fund.save()

        for expense in Expense.objects.all():
            if expense.received_date == datetime.date(1, 1, 1):  # This is possible because of our import script
                print("Changing dates for {}".format(expense))
                provisional_date = expense.fund.end_date + datetime.timedelta(30)
                expense.received_date = provisional_date
                expense.added = datetime.datetime(
                    provisional_date.year,
                    provisional_date.month,
                    provisional_date.day
                )
                expense.save()
