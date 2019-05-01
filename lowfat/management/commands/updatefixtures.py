from datetime import date, datetime

from django.core.management.base import BaseCommand

from lowfat.models import Claimant, Fund, Expense

class Command(BaseCommand):
    help = "Update Fixtures"

    def handle(self, *args, **options):
        new_year = date.today().year - 1
        last_year = None
        for claimant in Claimant.objects.filter().order_by('-application_year'):
            if last_year is None:
                last_year = claimant.application_year
            elif last_year != claimant.application_year:
                last_year = claimant.application_year
                new_year = new_year - 1

            claimant.application_year = new_year
            # TODO Update terms_and_conditions
            claimant.inauguration_grant_expiration = date(new_year + 2, 3, 31)
            claimant.save()

            for fund in Fund.objects.filter(
                    claimant=claimant
            ):
                fund.start_date = date(
                    new_year + 1,
                    fund.start_date.month,
                    fund.start_date.day
                )
                fund.end_date = date(
                    new_year + 1,
                    fund.end_date.month,
                    fund.end_date.day
                )
                fund.added = datetime(
                    new_year + 1,
                    fund.added.month,
                    fund.added.day,
                    fund.added.hour,
                    fund.added.minute
                )
                if fund.approved:
                    fund.approved = datetime(
                        new_year + 1,
                        fund.approved.month,
                        fund.approved.day,
                        fund.approved.hour,
                        fund.approved.minute
                    )
                fund.save()

                for expense in Expense.objects.filter(
                        fund=fund
                ):
                    expense.added = datetime(
                        new_year + 1,
                        expense.added.month,
                        expense.added.day,
                        expense.added.hour,
                        expense.added.minute
                    )
                    if expense.asked_for_authorization_date:
                        expense.asked_for_authorization_date = date(
                            new_year + 1,
                            expense.asked_for_authorization_date.month,
                            expense.asked_for_authorization_date.day
                        )
                    if expense.send_to_finance_date:
                        expense.send_to_finance_date = date(
                            new_year + 1,
                            expense.send_to_finance_date.month,
                            expense.send_to_finance_date.day
                        )
                    expense.save()
