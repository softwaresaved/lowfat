from datetime import date, timedelta
import pathlib

from django.test import TestCase
from django.core.files import File
from django.core.files.images import ImageFile

from . import (
    forms,
    models,
    testwrapper,
)

# Define the base directory for lowfat
BASE_DIR = pathlib.Path(__name__).absolute().parent


class FellowFormTest(TestCase):

    def test_blank_name(self):
        data = {
            "forenames": "",
            "surname": "",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_email(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": '',
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_phone(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_country(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_city(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_research_area(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "",
            "research_area_code": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertTrue(form.is_valid())

    def test_blank_research_area_code(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "research_area_code": "",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_affiliation(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "affiliation": "",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_funding(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "affiliation": "College",
            "funding": "",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_description(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_null_photo(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "research_area": "Y0",
            "affiliation": "College",
            "funding": "Self-funded",
            "work_description": "Work",
        }

        form = forms.FellowForm(data, {})
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "job_title_when_apply": "PhD",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "department": "Department",
            "group": "Group",
            "funding": "Self-funded",
            "funding_notes": "Self-funded",
            "interests": "foo",
            "work_description": "Work",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertTrue(form.is_valid())

    def test_expected(self):
        data = {
            "forenames": "C",
            "surname": "A",
            "email": "c.a@fake.lowfat.software.ac.uk",
            "phone": "+441111111111",
            "gender": "M",
            "home_country": "GB",
            "home_city": "L",
            "career_stage_when_apply": "2",
            "job_title_when_apply": "PhD",
            "research_area": "Y0",
            "research_area_code": "Y0",
            "affiliation": "College",
            "department": "Department",
            "group": "Group",
            "funding": "Self-funded",
            "funding_notes": "Self-funded",
            "interests": "foo",
            "work_description": "Work",
            "institutional_website": "http://ac.com/",
            "website": "http://ac.com/",
            "website_feed": "http://ac.com/feed.xml",
            "orcid": "ac",
            "google_scholar": "ac",
            "github": "ac",
            "gitlab": "ac",
            "bitbucket": "ac",
            "twitter": "ac",
            "linkedin": "ac",
            "facebook": "ac",
        }

        with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
            file_data = {
                "photo": ImageFile(test_image, name="ali-christensen.jpg")
            }

            form = forms.FellowForm(data, file_data)
        self.assertTrue(form.is_valid())


class FundFormTest(TestCase):
    def setUp(self):
        testwrapper.create_users()
        self.claimant_a_id, self.claimant_b_id = testwrapper.create_claimants()

    def test_null_claimant(self):
        data = {
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_claimant(self):
        data = {
            "claimant": "",
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_category(self):
        data = {
            "claimant": self.claimant_a_id,
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_focus(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_title(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_url(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
            "approval_chain": models.ApprovalChain.ONE_TIME.value,  # pylint: disable=no-member
        }

        form = forms.FundForm(data)
        self.assertTrue(form.is_valid())

    def test_blank_url(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
            "approval_chain": models.ApprovalChain.ONE_TIME.value,  # pylint: disable=no-member
        }

        form = forms.FundForm(data)
        self.assertTrue(form.is_valid())

    def test_not_http_url(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "fake",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
            "approval_chain": models.ApprovalChain.ONE_TIME.value,  # pylint: disable=no-member
        }

        form = forms.FundForm(data)
        self.assertTrue(form.is_valid())

    def test_null_country(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_country(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_city(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_city(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_start_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_start_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": "",
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_old_start_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() - timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_end_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_end_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": "",
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_old_end_date(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() - timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_travel(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_attendance_fees(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_subsistence_cost(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_request_venue_hire(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_catering(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_others(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_justification(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_justification(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": "",
            "success_targeted": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_success_targeted(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_success_targeted(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": "",
        }

        form = forms.FundForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
            "approval_chain": models.ApprovalChain.ONE_TIME.value,  # pylint: disable=no-member
        }

        form = forms.FundForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "claimant": self.claimant_a_id,
            "category": "A",
            "focus": "C",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today() + timedelta(1),
            "end_date": date.today() + timedelta(2),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "success_targeted": ":-)",
            "additional_info": "",
            "approval_chain": models.ApprovalChain.ONE_TIME.value,  # pylint: disable=no-member
        }

        form = forms.FundForm(data)
        self.assertTrue(form.is_valid())


class FundReviewFormTest(TestCase):
    def setUp(self):
        testwrapper.create_users()
        self.claimant_a_id, self.claimant_b_id = testwrapper.create_claimants()
        self.fund_id = testwrapper.create_fund(claimant_id=self.claimant_a_id).id

    def test_null_status(self):
        data = {
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_status(self):
        data = {
            "status": "",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_category(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_category(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_focus(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_focus(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "focus": "",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_fund_from_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_fund_from_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_grant(self):
        data = {
            "status": "",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_grant(self):
        data = {
            "status": "",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    # TODO uncomment in the future
    # def test_null_ad_status(self):
    #     data = {
    #         "status": "A",
    #         "category": "A",
    #         "focus": "C",
    #         "required_blog_posts": 1,
    #         "grant_heading": "F",
    #         "grant": "SSI1",
    #         "budget_approved": 100.00,
    #         "notes_from_admin": ":-)",
    #     }
    #
    #     form = forms.FundReviewForm(data)
    #     self.assertFalse(form.is_valid())
    #
    # def test_blank_ad_status(self):
    #     data = {
    #         "status": "A",
    #         "ad_status": "",
    #         "category": "A",
    #         "focus": "C",
    #         "grant_heading": "F",
    #         "grant": "SSI1",
    #         "required_blog_posts": 1,
    #         "budget_approved": 100.00,
    #         "notes_from_admin": ":-)",
    #     }
    #
    #     form = forms.FundReviewForm(data)
    #     self.assertFalse(form.is_valid())

    def test_null_required_blog_posts(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_null_budget_approved(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = forms.FundReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "category": "A",
            "focus": "C",
            "grant_heading": "F",
            "grant": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = forms.FundReviewForm(data)
        self.assertTrue(form.is_valid())


class ExpenseFormTest(TestCase):
    def setUp(self):
        testwrapper.create_users()
        self.claimant_a_id, self.claimant_b_id = testwrapper.create_claimants()
        self.fund_id = testwrapper.create_fund(claimant_id=self.claimant_a_id).id

    def test_null_fund(self):
        data = {
            "amount_claimed": 100.00,
        }

        with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
            file_data = {
                "claim": File(fake_file, name='ec1.pdf'),
            }

            form = forms.ExpenseForm(data, file_data)
            self.assertFalse(form.is_valid())

    def test_blank_fund(self):
        data = {
            "fund": "",
            "amount_claimed": 100.00,
        }

        with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
            file_data = {
                "claim": File(fake_file, name='ec1.pdf'),
            }

            form = forms.ExpenseForm(data, file_data)
            self.assertFalse(form.is_valid())

    def test_null_amount_claimed(self):
        data = {
            "fund": self.fund_id,
        }

        with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
            file_data = {
                "claim": File(fake_file, name='ec1.pdf'),
            }

            form = forms.ExpenseForm(data, file_data)
            self.assertFalse(form.is_valid())

    def test_null_claim(self):
        data = {
            "fund": self.fund_id,
            "amount_claimed": 100.00,
        }

        form = forms.ExpenseForm(data)
        self.assertFalse(form.is_valid())

    # def test_full_expected(self):
    #     data = {
    #         "fund": self.fund_id,
    #         "amount_claimed": 100.00,
    #     }

    #     with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
    #         file_data = {
    #             "claim": File(fake_file, name='ec1.pdf'),
    #             "receipts": File(fake_file, name='ec1-receipts.pdf')
    #         }
    #         form = forms.ExpenseForm(data, file_data)
    #         self.assertTrue(form.is_valid())


class ExpenseReviewFormTest(TestCase):
    def setUp(self):
        self.claimant_test_data = testwrapper.create_all()
        # unpack outputs of create_all here for ease of use later
        self.claimant_id_a = self.claimant_test_data['claimant-a']['claimant_id']
        self.fund_id_a = self.claimant_test_data['claimant-a']['fund_id']
        self.expense_id_a = self.claimant_test_data['claimant-a']['expense_id']
        self.blog_id_a = self.claimant_test_data['claimant-a']['blog_id']

    def test_grant_heading(self):
        for fund in ['C', 'I', 'F']:
            data = {
                "status": "S",
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "grant_heading": fund,
                "grant": "SSI1",
            }

            form = forms.ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_grant(self):
        for grant in ['SSI1', 'SSI2', 'SSI3']:
            data = {
                "status": "S",
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "grant_heading": "F",
                "grant": grant,
            }

            form = forms.ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_expense_status(self):
        for status in ('S', 'C', 'A', 'R', 'X'):
            data = {
                "status": status,
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "grant_heading": "F",
                "grant": "SSI1",
            }

            form = forms.ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "status": "S",
            "asked_for_authorization_date": "2016-01-01",
            "send_to_finance_date": "2016-01-01",
            "amount_authorized_for_payment": 100.00,
            "grant_heading": "F",
            "grant": "SSI1",
        }

        form = forms.ExpenseReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "status": "S",
            "asked_for_authorization_date": "2016-01-01",
            "send_to_finance_date": "2016-01-01",
            "amount_authorized_for_payment": 100.00,
            "grant_heading": "F",
            "grant": "SSI1",
            "notes_from_admin": ":-)",
        }

        form = forms.ExpenseReviewForm(data)
        self.assertTrue(form.is_valid())


class BlogFormTest(TestCase):
    def setUp(self):
        testwrapper.create_users()
        self.claimant_a_id, self.claimant_b_id = testwrapper.create_claimants()
        self.fund_id = testwrapper.create_fund(claimant_id=self.claimant_a_id).id

    def test_null_draft_url(self):
        data = {
            "fund": self.fund_id,
            "final": True,
        }

        form = forms.BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_draft_url(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "",
            "final": True,
        }

        form = forms.BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_null_final(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "https://www.software.ac.uk/",
        }

        form = forms.BlogForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "https://www.software.ac.uk/",
            "notes_from_author": "Notes",
            "final": True,
        }

        form = forms.BlogForm(data)
        self.assertTrue(form.is_valid())


class BlogReviewFormTest(TestCase):
    def setUp(self):
        self.claimant_test_data = testwrapper.create_all()
        # unpack outputs of create_all here for ease of use later
        self.claimant_id_a = self.claimant_test_data['claimant-a']['claimant_id']
        self.fund_id_a = self.claimant_test_data['claimant-a']['fund_id']
        self.expense_id_a = self.claimant_test_data['claimant-a']['expense_id']
        self.blog_id_a = self.claimant_test_data['claimant-a']['blog_id']

    def test_blog_status(self):
        for status in ('U', 'R', 'L', 'P', 'D', 'O'):
            data = {
                "draft_url": "https://www.software.ac.uk/",
                "status": status,
                "published_url": "https://www.software.ac.uk/",
            }

            form = forms.BlogReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "draft_url": "https://www.software.ac.uk/",
            "status": "P",
            "published_url": "https://www.software.ac.uk/",
        }

        form = forms.BlogReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "draft_url": "https://www.software.ac.uk/",
            "status": "P",
            "published_url": "https://www.software.ac.uk/",
            "title": "Title",
            "notes_from_admin": ":-)",
        }

        form = forms.BlogReviewForm(data)
        self.assertTrue(form.is_valid())
