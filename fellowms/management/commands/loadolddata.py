import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from fellowms.models import Fellow, Event

# TODO Add others files
APPLICANTS_CSV = "data/applicants.csv"
INFO_CSV = "data/info.csv"
EVENTS_CSV = "data/events.csv"

def show_row_with_problem(exception, row):
    print("""
================================================================================
{}
--------------------------------------------------------------------------------

{}

================================================================================
""".format(exception, row))

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
                facebook="")

        # FIXME The script must be more stable.
        try:
            fellow.save()
        except Exception as e:
            show_row_with_problem(e, row)

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
    data = pd.read_csv(EVENTS_CSV)

    for index, row in data.iterrows():
        try:
            fullname = row["Fellow name"].strip().split(" ")
            surname = fullname[-1]
            forenames = " ".join(fullname[:-1])

            fellow = Fellow.objects.get(
                    forenames=forenames,
                    surname=surname)

            category = "O"
            if row["Event type"] == "Attending a conference/workshop":
                category = "A"
            elif row["Event type"] == "Organising a workshop (e.g. Software Carpentry)":
                category = "H"

            if row["Approved"] == "Yes":
                budget_approve = True
            else:
                budget_approve = False

            event = Event(
                    fellow=fellow,
                    category=category,
                    name=row["Event name"],
                    url=row["Event website"],
                    location=row["Event location"],
                    start_date=pd.to_datetime(row['Start date'], format='%d/%m/%Y'),
                    end_date=pd.to_datetime(row['End date'], format='%d/%m/%Y'),
                    budget_request_travel=row["Travel costs"],
                    budget_request_attendance_fees=row["Conference/Workshop attendance fees"],
                    budget_request_subsistence_cost=row["Subsistence costs"],
                    budget_request_venue_hire=row["Venue hire"],
                    budget_request_catering=row["Catering"],
                    budget_request_others=row["Other costs"],
                    budget_approve=budget_approve,
                    justification=row["How is the event relevant to the work of the Software Sustainability Institute?"],
                    additional_info=row["Any other information relevant to this application?"],
                    status="A"  # FIXME
                    )

            # FIXME The script must be more stable.
            event.save()
        except Exception as e:
            show_row_with_problem(e, row)

class Command(BaseCommand):
    help = "Add old information to database."

    # TODO Make use of args and options.
    def handle(self, *args, **options):
        handle_applicants()
        handle_info()
        handle_events()
