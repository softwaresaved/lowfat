import urllib.request

import pandas as pd

from django.core.files import File
from django.core.management.base import BaseCommand

from lowfat.models import Claimant

class Command(BaseCommand):
    help = "Import CSV (old_applications.csv) with applications to claimantship to the database."

    def add_arguments(self, parser):
        parser.add_argument('csv', nargs='?', default='old_applications.csv')

    def handle(self, *args, **options):
        data = pd.read_csv(options['csv'])
        for index, line in data.iterrows():  # pylint: disable=no-member,unused-variable
            try:
                is_fellow = line['Selected'] == 'Yes'

                if pd.notnull(line["Photo"]):
                    photo_name, photo_info = urllib.request.urlretrieve(line["Photo"])  # pylint: disable=unused-variable
                    photo = File(open(photo_name, "rb"))
                    photo.name = line["Photo"].split("/")[-1]
                else:
                    photo = None

                if pd.notnull(line["Research classification"]):
                    jacs = "{}00".format(line["Research classification"][0:2])
                else:
                    jacs = "Y000"

                applicants_dict = {
                    "application_year": line["Inauguration year"] - 1,
                    "fellow": is_fellow,
                    "forenames": line["Forename(s)"],
                    "surname": line["Surname"],
                    "affiliation": line["Home institution"],
                    "research_area": line["Research area"],
                    "research_area_code": jacs,
                    "email": line["E-mail"],
                    "phone": line["Telephone"],
                    "gender": line["Gender"] if pd.notnull(line["Gender"]) else 'R',
                    "home_country": "GB",
                    "home_city": "SSI",
                    "work_description": line["Work area"],
                    "funding": "{}, {}".format(line["Primary funder"], line["Additional funder"]),
                    "claimantship_grant": 3000 if is_fellow else 0,
                }

                if photo:
                    applicants_dict.update({
                        "photo": photo,
                        })

                applicant = Claimant(**applicants_dict)
                applicant.save()

            except BaseException as exception:
                print("Error: {}\n\t{}".format(exception, line))
