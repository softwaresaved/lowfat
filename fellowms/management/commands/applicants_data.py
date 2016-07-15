import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from fellowms.models import Fellow

class Command(BaseCommand):
    help = "Add old information to database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        data =  pd.read_csv('all_applications_details.csv')
        for idx, line in data.iterrows():
            if line['Selected']=='Yes':
                is_fellow=True
            else:
                is_fellow=False
            applicants_dict = {
                    "application_year": line["Inauguration year"],
                    "selected": is_fellow,
                    "forenames": line["Forename(s)"],
                    "surname": line["Surname"],
                    "affiliation": line["Home institution"],
                    "research_area": line["Research area"],
                    "research_area_code": line["Research classification"],
                    "email": line["E-mail"],
                    "phone": line["Telephone"],
                    "gender": line["Gender"] if line["Gender"] else 'R',
                    "work_description": line["Work area"],
                    "funding": "{}, {}".format(line["Primary funder"],line["Additional funder"]),
                }
            applicant = Fellow(**applicants_dict)
            applicant.save()
