import pandas as pd

from django.core.management.base import BaseCommand

from lowfat.models import Fund

class Command(BaseCommand):
    help = "Add activities"

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
                    if line["category"] == "Organising":
                        fund.category = "H"
                    elif line["category"] == "Attending":
                        fund.category = "A"

                    if line["focus"] == "Domain":
                        fund.focus = "D"
                    elif line["focus"] == "Cross_cutting":
                        fund.focus = "C"

                    if pd.notnull(line["activities"]):
                        fund.activity = line["activities"]

                    print("Changing {}...".format(fund))
                    fund.save()
                    print("Changed {}...".format(fund))

            except BaseException as exception:
                print("Error: {}\n\t{}".format(exception, line))
