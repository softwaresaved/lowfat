import pandas as pd

from django.core.management.base import BaseCommand

from lowfat.models import Fund, Expense

class Command(BaseCommand):
    help = "Fix funding source"

    def add_arguments(self, parser):
        parser.add_argument('csv', nargs='?', default='funds.csv')

    # pylint: disable=too-many-branches,too-many-locals
    def handle(self, *args, **options):
        data = pd.read_csv(options['csv'])
        for index, line in data.iterrows():  # pylint: disable=no-member,unused-variable
            try:
                funds = Fund.objects.filter(
                    claimant__forenames=line["forname_s"],
                    claimant__surname=line["surname"],
                    title=line["event_title"]
                    )
                for fund in funds:
                    fund.funds_from_default = line["new_funding_source_subcategory"]
                    fund.grant_default = line["funding_source"]
                    print("Changing {}...".format(fund))
                    fund.save()
                    print("Changed {}...".format(fund))

                    for expense in Expense.objects.filter(fund=fund):
                        expense.funds_from = line["new_funding_source_subcategory"]
                        expense.grant_used = line["funding_source"]
                        print("Changing {}...".format(expense))
                        expense.save()
                        print("Changed {}...".format(expense))

            except BaseException as exception:
                print("Error: {}\n\t{}".format(exception, line))
