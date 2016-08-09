import urllib.request

import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from fat.models import Fellow

CSV_TO_IMPORT = 'old_applications.csv'

class Command(BaseCommand):
    help = "Import CSV (old_applications.csv) with applications to fellowship to the database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        data =  pd.read_csv(CSV_TO_IMPORT)
        for idx, line in data.iterrows():
            try:
                if line['Selected']=='Yes':
                    is_fellow=True
                else:
                    is_fellow=False

                if pd.notnull(line["Photo"]):
                    photo_name, photo_info = urllib.request.urlretrieve(line["Photo"])
                    photo = File(open(photo_name, "rb"))
                    photo.name = line["Photo"].split("/")[-1]

                if pd.notnull(line["Research classification"]):
                    jacs = "{}00".format(line["Research classification"][0:2])
                else:
                    jacs = "Y000"

                applicants_dict = {
                    "application_year": line["Inauguration year"],
                    "selected": is_fellow,
                    "forenames": line["Forename(s)"],
                    "surname": line["Surname"],
                    "affiliation": line["Home institution"],
                    "research_area": line["Research area"],
                    "research_area_code": jacs,
                    "email": line["E-mail"],
                    "phone": line["Telephone"],
                    "gender": line["Gender"] if pd.notnull(line["Gender"]) else 'R',
                    "home_location": "UK",
                    "home_lon": 0,
                    "home_lat": 51,
                    "work_description": line["Work area"],
                    "funding": "{}, {}".format(line["Primary funder"],line["Additional funder"]),
                    "fellowship_grant": 3000 if is_fellow else 0,
                }

                if photo:
                    applicants_dict.update({
                        "photo": photo,
                        })

                applicant = Fellow(**applicants_dict)
                applicant.save()

            except BaseException as e:
                print("Error: {}\n\t{}".format(e, line))