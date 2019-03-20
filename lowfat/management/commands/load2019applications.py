import pandas as pd

from django.contrib.auth.models import User, BaseUserManager
from django.core.management.base import BaseCommand

from lowfat.models import Claimant

class Command(BaseCommand):
    help = "Import CSV with 2019 applications."

    def add_arguments(self, parser):
        parser.add_argument('csv', nargs='?', default='2019.csv')

    # pylint: disable=too-many-branches,too-many-locals
    def handle(self, *args, **options):
        fail_list = []
        success_list = []
        user_manager = BaseUserManager()

        data = pd.read_csv(options['csv'])
        for index, line in data.iterrows():  # pylint: disable=no-member,unused-variable
            try:
                received_offer = line['Invited'] == 'YES'
                if line["Research Classification"] == "N/A - I do not do research":
                    jacs = "Y0"
                else:
                    jacs = line["Research Classification"][1:3]

                applicants_dict = {
                    "application_year": 2018,
                    "fellow": False,
                    "received_offer": received_offer,
                    "forenames": line["First name"],
                    "surname": line["Surname"],
                    "affiliation": line["Home Institution"],
                    "department": line["Department"] if pd.notnull(line["Department"]) else "",
                    "group": line["Group within Department"] if pd.notnull(line["Group within Department"]) else "",
                    "career_stage_when_apply": line["Career stage"][6],
                    "job_title_when_apply": line["Job Title"],
                    "research_area": line["Area of work"],
                    "research_area_code": jacs,
                    "email": line["Email Address"],
                    "phone": line["Telephone number"],
                    "gender": line["Gender"][0] if pd.notnull(line["Gender"]) else 'R',
                    "home_country": "GB",
                    "home_city": "Unknow",
                    "funding": line["Which primary funding body/charity/organisation would you normally turn to if seeking financial support for your research/work"],
                    "funding_notes": line["Which additional funding body/charity/organisation would you probably turn to if seeking financial support for your research/work"] if pd.notnull(line["Which additional funding body/charity/organisation would you probably turn to if seeking financial support for your research/work"]) else "",
                    "claimantship_grant": 3000 if received_offer else 0,
                    "institutional_website": line["Please specify your Institutional webpage"] if pd.notnull(line["Please specify your Institutional webpage"]) else "",
                    "website": line["Please specify your blog"] if pd.notnull(line["Please specify your blog"]) else "",
                    "orcid": line["Please specify your ORCID"] if pd.notnull(line["Please specify your ORCID"]) else "",
                    "google_scholar": line["Please specify your Google Scholar"] if pd.notnull(line["Please specify your Google Scholar"]) else "",
                    "twitter": line["Please specify your Twitter handle"] if pd.notnull(line["Please specify your Twitter handle"]) else "",
                    "screencast_url": line["Application Screencast URL"] if pd.notnull(line["Application Screencast URL"]) else "",
                    "example_of_writing_url": line["Example of writing"] if pd.notnull(line["Example of writing"]) else "",
                }

                applicant = Claimant(**applicants_dict)
                applicant.save()
                success_list.append(index)

                if received_offer:
                    new_user = User.objects.create_user(
                        username=applicant.slug,
                        email=applicant.email,
                        password=user_manager.make_random_password(),
                        first_name=line["First name"],
                        last_name=line["Surname"]
                    )
                    applicant.user = new_user
                    applicant.save()

            except BaseException as exception:
                print("Error: {}\n{}\n{}".format(exception, line, 80 * "-"))
                fail_list.append(index)

        print(80 * "-")
        print("Success: {}".format(success_list))
        print("Fail: {}".format(fail_list))
