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
                        "location": line["Event location"],
                        "start_date": conv_date(line["Start date"]),
                        "end_date": conv_date(line["End date"]) if line["End date"] else conv_date(line["Start date"]),
                        "budget_request_travel": line["Travel costs"] if pd.notnull(line["Travel costs"]) else 0,
                        "budget_request_attendance_fees": line["Conference/Workshop attendance fees"] if pd.notnull(line["Conference/Workshop attendance fees"]) else 0,
                        "budget_request_subsistence_cost": line["Subsistence costs"] if pd.notnull(line["Subsistence costs"]) else 0,
                        "budget_request_venue_hire": line["Venue hire"] if pd.notnull(line["Venue hire"]) else 0,
                        "budget_request_catering": line["Catering"] if pd.notnull(line["Catering"]) else 0,
                        "budget_request_others": line["Other costs"] if pd.notnull(line["Other costs"]) else 0,
                        "budget_approved": line["Estimate"] if pd.notnull(line["Estimate"]) else 0,
                        "justification": line["How is the event relevant to the work of the Software Sustainability Institute?"],
                }
                event = Event(**events_dict)
                event.save()
                if line["Revised estimate"]:
                    expense_dict = {
                        "event": event,
                        "amount_claimed": line["Revised estimate"] if pd.notnull(line["Revised estimate"]) else 0,
                    }
                    expense = Expense(**expense_dict)
                    expense.save()
            except BaseException as e:
                print("Error: {}\n\t{}".format(e, line))
