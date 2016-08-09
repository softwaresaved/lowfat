import io

import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError

from fat.models import Fellow, Event, Expense

CSV_TO_IMPORT = 'old_funds.csv'

def conv_date(new_date):
    day, month, year = new_date.split('/')
    return "{}-{}-{}".format(year, month, day)

class Command(BaseCommand):
    help = "Import CSV (old_funds.csv) with funds from fellows to the database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        data =  pd.read_csv(CSV_TO_IMPORT)
        for idx, line in data.iterrows():
            try:
                this_fellow = Fellow.objects.get(forenames=line["Forename(s)"], surname=line["Surname"], selected=True)
                if line['Event type'] == 'Attending a conference/workshop':
                    fund_category = 'A'
                elif line['Event type'] == ' Organising a workshop (e.g. Software Carpentry)':
                    fund_category = 'H'
                elif line['Event type'] == 'Policy related fund':
                    fund_category = 'P'
                else:
                    fund_category = 'O'
                funds_dict = {
                        "fellow": this_fellow,
                        "category": fund_category,
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
                        "justification": line["How is the fund relevant to the work of the Software Sustainability Institute?"],
                        "notes_from_admin": "{}\n{}\n{}".format(
                            line["Notes A"] if pd.notnull(line["Notes A"]) else "",
                            line["Notes B"] if pd.notnull(line["Notes B"]) else "",
                            line["Notes C"] if pd.notnull(line["Notes C"]) else "")
                }
                fund = Event(**funds_dict)
                fund.save()
                if pd.notnull(line['Approved']) and line['Approved'] != 'N/A':
                    fund.ad_status = 'V'
                    fund.status = 'A'
                    fund.save()
                if pd.notnull(line["Revised estimate"]):
                    expense_dict = {
                        "fund": fund,
                        "amount_claimed": line["Revised estimate"] if pd.notnull(line["Revised estimate"]) else 0,
                        "received_date": '0001-01-01',
                    }

                    with io.BytesIO(b"""# Missing document

The document that you are looking for doesn't exist because

1. it wasnr't send to us,
2. it is stored only as paper copy in our archives,
3. it is stored on our SVN server, or
4. it is stored on our Google Drive account.

Sorry for the inconvenience.""") as fake_file:
                        expense_dict.update({
                            "claim": SimpleUploadedFile('missing-proof.pdf', fake_file.read()),
                        })

                    expense = Expense(**expense_dict)
                    expense.save()
                    if line['Claim'] in ['Yes', 'SVN', 'Partial', 'Hard copy', 'Ask accounts for copy of invoice'] and pd.notnull(line['Authorised']):
                        expense.funds_from = line["Type"] if pd.notnull(line["Type"]) else 'C'
                        expense.status = 'A'
                        expense.amount_authorized_for_payment = line["Revised estimate"]
                        expense.save()
                        fund.status = 'F'
                        fund.save()
            except BaseException as e:
                print("Error: {}\n\t{}".format(e, line))
