from datetime import date
import io

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .testwrapper import *
from .models import *
from .forms import *

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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        form = FellowForm(data, {})
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
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

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
        self.assertTrue(form.is_valid())

class FundFormTest(TestCase):
    def setUp(self):
        self.claimant_id = create_claimant()

    def test_null_claimant(self):
        data = {
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_claimant(self):
        data = {
            "claimant": "",
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_title(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_title(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_url(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertTrue(form.is_valid())

    def test_blank_url(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertTrue(form.is_valid())

    def test_not_http_url(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "fake",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertTrue(form.is_valid())

    def test_null_country(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_country(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_city(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_city(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_start_date(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_start_date(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": "",
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_end_date(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_end_date(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": "",
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_travel(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_attendance_fees(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_subsistence_cost(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_request_venue_hire(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_catering(self):  # pylint: disable=invalid-name
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_others(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_null_justification(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_justification(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": "",
        }

        form = FundForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
        }

        form = FundForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "claimant": self.claimant_id,
            "category": "A",
            "title": "Fake",
            "url": "http://fake.com",
            "country": "GB",
            "city": "L",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            "additional_info": "",
        }

        form = FundForm(data)
        self.assertTrue(form.is_valid())

class FundReviewFormTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id = create_fund()

    def test_null_status(self):
        data = {
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_status(self):
        data = {
            "status": "",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_fund_from_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_fund_from_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "funds_from_default": "",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_grant_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "funds_from_default": "F",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_grant_default(self):
        data = {
            "status": "",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    # TODO uncomment in the future
    #def test_null_ad_status(self):
    #    data = {
    #        "status": "A",
    #        "required_blog_posts": 1,
    #        "funds_from_default": "F",
    #        "grant_default": "SSI1",
    #        "budget_approved": 100.00,
    #        "notes_from_admin": ":-)",
    #    }
    #
    #    form = FundReviewForm(data)
    #    self.assertFalse(form.is_valid())
    #
    #def test_blank_ad_status(self):
    #    data = {
    #        "status": "A",
    #        "ad_status": "",
    #        "funds_from_default": "F",
    #        "grant_default": "SSI1",
    #        "required_blog_posts": 1,
    #        "budget_approved": 100.00,
    #        "notes_from_admin": ":-)",
    #    }
    #
    #    form = FundReviewForm(data)
    #    self.assertFalse(form.is_valid())

    def test_null_required_blog_posts(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "budget_approved": 100.00,
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_approved(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
        }

        form = FundReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "funds_from_default": "F",
            "grant_default": "SSI1",
            "required_blog_posts": 1,
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
        }

        form = FundReviewForm(data)
        self.assertTrue(form.is_valid())


class ExpenseFormTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id = create_fund()

    def test_null_fund(self):
        data = {
            "amount_claimed": 100.00,
        }

        with open("upload/expenses/ec1.pdf", "rb") as fake_file:
            file_data = {
                "claim": SimpleUploadedFile('claim.pdf', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_fund(self):
        data = {
            "fund": "",
            "amount_claimed": 100.00,
        }

        with open("upload/expenses/ec1.pdf", "rb") as fake_file:
            file_data = {
                "claim": SimpleUploadedFile('claim.pdf', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_null_amount_claimed(self):
        data = {
            "fund": self.fund_id,
        }

        with open("upload/expenses/ec1.pdf", "rb") as fake_file:
            file_data = {
                "claim": SimpleUploadedFile('claim.pdf', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_null_claim(self):
        data = {
            "fund": self.fund_id,
            "amount_claimed": 100.00,
        }

        form = ExpenseForm(data)
        self.assertFalse(form.is_valid())

    def test_full_expected(self):
        data = {
            "fund": self.fund_id,
            "amount_claimed": 100.00,
        }

        with open("upload/expenses/ec1.pdf", "rb") as fake_file:
            file_data = {
                "claim": SimpleUploadedFile('claim.pdf', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertTrue(form.is_valid())

class ExpenseReviewFormTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id, self.expense_id, self.blog_id = create_all()

    def test_funds_from(self):
        for fund in ['C', 'I', 'F']:
            data = {
                "status": "S",
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "funds_from": fund,
                "grant_used": "SSI1",
            }

            form = ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_grant_used(self):
        for grant in ['SSI1', 'SSI2', 'SSI3']:
            data = {
                "status": "S",
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "funds_from": "F",
                "grant_used": grant,
            }

            form = ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_expense_status(self):
        for status in ('W', 'S', 'C', 'P', 'A', 'F'):
            data = {
                "status": status,
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "funds_from": "F",
                "grant_used": "SSI1",
            }

            form = ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())


    def test_minimal_expected(self):
        data = {
            "status": "S",
            "asked_for_authorization_date": "2016-01-01",
            "send_to_finance_date": "2016-01-01",
            "amount_authorized_for_payment": 100.00,
            "funds_from": "F",
            "grant_used": "SSI1",
        }

        form = ExpenseReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "status": "S",
            "asked_for_authorization_date": "2016-01-01",
            "send_to_finance_date": "2016-01-01",
            "amount_authorized_for_payment": 100.00,
            "funds_from": "F",
            "grant_used": "SSI1",
            "notes_from_admin": ":-)",
        }

        form = ExpenseReviewForm(data)
        self.assertTrue(form.is_valid())


class BlogFormTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id = create_fund()

    def test_null_draft_url(self):
        data = {
            "fund": self.fund_id,
            "final": True,
        }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_draft_url(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "",
            "final": True,
        }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_null_final(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "https://www.software.ac.uk/",
        }

        form = BlogForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "fund": self.fund_id,
            "draft_url": "https://www.software.ac.uk/",
            "notes_from_author": "Notes",
            "final": True,
        }

        form = BlogForm(data)
        self.assertTrue(form.is_valid())

class BlogReviewFormTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id, self.expense_id, self.blog_id = create_all()

    def test_blog_status(self):
        for status in ('U', 'R', 'L', 'P', 'D', 'O'):
            data = {
                "draft_url":  "https://www.software.ac.uk/",
                "status": status,
                "published_url": "https://www.software.ac.uk/",
            }

            form = BlogReviewForm(data)
            self.assertTrue(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "draft_url":  "https://www.software.ac.uk/",
            "status": "P",
            "published_url": "https://www.software.ac.uk/",
        }

        form = BlogReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "draft_url":  "https://www.software.ac.uk/",
            "status": "P",
            "published_url": "https://www.software.ac.uk/",
            "title": "Title",
            "notes_from_admin": ":-)",
        }

        form = BlogReviewForm(data)
        self.assertTrue(form.is_valid())
