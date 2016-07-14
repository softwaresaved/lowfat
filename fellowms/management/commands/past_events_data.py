import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from fellowms.models import Fellow, Event, Expense

def conv_date(new_date):
    day, month, year = new_date.split('/')
    return "{}-{}-{}".format(year, month, day)

class Command(BaseCommand):
    help = "Upload old event data to the database"

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        data =  pd.read_csv('fellows_events.csv')
        for idx, line in data.iterrows():
            try:
                this_fellow = Fellow.objects.get(forenames=line["Forename(s)"], surname=line["Surname"], selected=True)
                events_dict = {
                        "fellow": this_fellow,
                        "name": line["Event name"],
                        "url": line["Event website"],
                        "location": ["Event location"],
                        "start_date": conv_date(line["Start date"]),
                        "end_date": conv_date(line["End date"]) if line["End date"] else conv_date(line["Start date"]),
                        "budget_approved": line["Estimate"],
                        "justification": line["How is the event relevant to the work of the Software Sustainability Institute?"],
                }
                event = Event(**events_dict)
                event.save()
                expense_dict = {
                        "event": event,
                        "amount_claimed": line["Revised estimate"]
                    }
                expense = Expense(**expense_dict)
                expense.save()
            except BaseException as e:
                print("Error: {}".format(e))
                print("{} {}".format(line["Forename(s)"], line["Surname"]))
                print("{} {}".format(line["Start date"], line["End date"]))