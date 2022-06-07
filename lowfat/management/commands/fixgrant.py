import pandas as pd

from django.core.management.base import BaseCommand

from lowfat.models import Fund


class Command(BaseCommand):
    help = "Fix grant"

    def add_arguments(self, parser):
        parser.add_argument('csv', nargs='?', default='activities.csv')

    # pylint: disable=too-many-branches,too-many-locals
    def handle(self, *args, **options):
        data = pd.read_csv(options['csv'])
        for index, line in data.iterrows():  # pylint: disable=no-member,unused-variable
            try:
                funds = Fund.objects.filter(
                    claimant__forenames=line["fornames"],
                    claimant__surname=line["surname"],
                    title=line["title"]
                )

                for fund in funds:
                    fund.grant = line["grant"]
                    if line["grant_heading"] == "Fellowship":
                        fund.grant_heading = "F"
                    elif line["grant_heading"] == "Core":
                        fund.grant_heading = "I"
                    elif line["grant_heading"] == "Continuing":
                        fund.grant_heading = "C"

                    print("Changing {}...".format(fund))
                    fund.save()
                    print("Changed {}...".format(fund))

            except BaseException as exception:
                print("Error: {}\n\t{}".format(exception, line))
