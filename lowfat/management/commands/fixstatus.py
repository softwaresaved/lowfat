import datetime

from django.core.management.base import BaseCommand

from lowfat.models import FUND_STATUS_APPROVED_SET, Fund, Expense

class Command(BaseCommand):
    help = "Fix the status on the database."

    def handle(self, *args, **options):
        # Blog posts
        # Nothing to change

        # Expense status
        # Nothing to change

        # Fund status
        # Move approved to archived
        for fund in Fund.objects.filter(status__in=FUND_STATUS_APPROVED_SET).all():
            day = datetime.timedelta(1)
            if fund.added - datetime.datetime(2017, 12, 31) < day:
                # Check for expenses
                # Check for blog posts
                print("Changing status for {}".format(fund))
                fund.status = "F"
                fund.save()
            else:
                can_be_archive = True
                expenses = Expense.objects.filter(
                    fund=fund,
                )
                if not expenses:
                    can_be_archive = False
                for expense in expenses:
                    if expense.status in ["S", "C"]:
                        can_be_archive = False
                        break
                if can_be_archive:
                    print("Changing status for {}".format(fund))
                    fund.status = "F"
                    fund.save()
