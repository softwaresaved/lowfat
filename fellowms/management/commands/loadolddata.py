import pandas as pd

from django.core.management.base import BaseCommand, CommandError

from fellowms.models import Fellow

# TODO Add others files
CSV_FILEAME = "data/applicants.csv"

class Command(BaseCommand):
    help = "Add old information to database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        data = pd.read_csv(CSV_FILEAME)

        for index, row in data.iterrows():
            fellow = Fellow(
                    forenames=row["Forename(s)"],
                    surname=row["Surname"],
                    email=row["E-mail"],
                    phone=row["Telephone number"],
                    gender=row["Gender"],
                    home_location="",
                    photo="blank.jpg",
                    research_area=row["Research area"],
                    affiliation=row["Home institution"],
                    funding=row["Primary funder"],
                    work_description=row["Describe your work"],
                    website="",
                    website_feed="",
                    orcid="",
                    github="",
                    gitlab="",
                    twitter="",
                    facebook="",
                    inauguration_year=row["Year"])

            # FIXME The script must be more stable.
            try:
                fellow.save()
            except:
                pass
