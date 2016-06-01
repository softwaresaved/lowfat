import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from fellowms.models import Fellow

# TODO Add others files
APPLICANTS_CSV = "data/applicants.csv"
INFO_CSV = "data/info.csv"
EVENTS_CSV = "data/events.csv"

def handle_applicants():
    data = pd.read_csv(APPLICANTS_CSV)

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

def handle_info():
    data = pd.read_csv(INFO_CSV)

    for index, row in data.iterrows():
        fullname = row["Fellow"].strip().split(" ")
        surname = fullname[-1]
        forenames = " ".join(fullname[:-1])

        funding = "{}, {}".format(
                row["Funding (self-reported)"],
                row["funding (google)"])

        # XXX The is some problem with the data. :-(
        home_lon = row["Home Longitude"]
        if type(home_lon) != float:
            home_lon = home_lon[0]
        home_lat = row["Home Latitude"]
        if type(home_lat) != float:
            home_lat = home_lat[0]

        try:
            # XXX This can create duplicates.
            fellow = Fellow.objects.get(
                    forenames=forenames,
                    surname=surname)

            fellow.inauguration_year = row["Inauguration year"]
            fellow.home_location = row["Home Location"],
            fellow.home_lon = home_lon
            fellow.home_lat = home_lat
            fellow.research_area = row["HESA JACS3 Level 2 Code"],
            fellow.affiliation = row["Home institution"],
        except ObjectDoesNotExist as e:
            fellow = Fellow(
                    forenames=forenames,
                    surname=surname,
                    email="{}.{}@missing.com".format(forenames, surname),
                    phone="{}{}".format(forenames[0], surname[0]),
                    gender='R',
                    home_location=row["Home Location"],
                    home_lon=home_lon,
                    home_lat=home_lat,
                    photo="blank.jpg",
                    research_area=row["HESA JACS3 Level 2 Code"],
                    affiliation=row["Home institution"],
                    funding=funding,
                    work_description="",
                    website="",
                    website_feed="",
                    orcid="",
                    github="",
                    gitlab="",
                    twitter="",
                    facebook="",
                    inauguration_year=row["Inauguration year"])

        fellow.save()

def handle_events():
    data = pd.read_csv(INFO_CSV)

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

class Command(BaseCommand):
    help = "Add old information to database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        handle_applicants()
        handle_info()
        # handle_events()
