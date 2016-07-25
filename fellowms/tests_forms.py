from datetime import date
import io
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from .testwrapper import *
from .models import *
from .forms import *

class FellowFormTest(unittest.TestCase):
    def test_blank_name(self):
        data = {
        "forenames": "",
        "surname": "",
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
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
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
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

    def test_blank_location(self):
        data = {
        "forenames": "C",
        "surname": "A",
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "",
        "research_area": "Y000",
        "research_area_code": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "",
        "research_area_code": "Y000",
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

    def test_blank_research_area_code(self):
        data = {
        "forenames": "C",
        "surname": "A",
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
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
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
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

    def test_expected(self):
        data = {
        "forenames": "C",
        "surname": "A",
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
        "affiliation": "College",
        "funding": "Self-funded",
        "work_description": "Work",
        "website": "http://ac.com/",
        "website_feed": "http://ac.com/feed.xml",
        "orcid": "ac",
        "github": "ac",
        "gitlab": "ac",
        "twitter": "ac",
        "facebook": "ac",
            }

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            }

        form = FellowForm(data, file_data)
        self.assertTrue(form.is_valid())

class EventFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id = create_fellow()

    def test_null_fellow(self):
        data = {
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_fellow(self):
        data = {
            "fellow": "",
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_name(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_name(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())
        
    def test_null_url(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_url(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_not_http_url(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "fake",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_location(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_location(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_start_date(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_start_date(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_end_date(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_end_date(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": "",
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_travel(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_attendance_fees(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_subsistence_cost(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_request_venue_hire(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_catering(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_others": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_request_others(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "justification": ":-)",
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_null_justification(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": date.today(),
            "end_date": date.today(),
            "budget_request_travel": 100.00,
            "budget_request_attendance_fees": 0.00,
            "budget_request_subsistence_cost": 0.00,
            "budget_request_venue_hire": 0.00,
            "budget_request_catering": 0.00,
            "budget_request_others": 0.00,
            }

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_justification(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "fellow": self.fellow_id,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
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

        form = EventForm(data)
        self.assertTrue(form.is_valid())

class EventReviewFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id, self.event_id = create_event()

    def test_null_status(self):
        data = {
            "ad_status": "V",
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_status(self):
        data = {
            "status": "",
            "ad_status": "V",
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_add_status(self):
        data = {
            "status": "A",
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_ad_status(self):
        data = {
            "status": "A",
            "ad_status": "",
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_null_budget_approved(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_minimal_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "budget_approved": 100.00,
            }

        form = EventReviewForm(data)
        self.assertTrue(form.is_valid())

    def test_full_expected(self):
        data = {
            "status": "A",
            "ad_status": "V",
            "budget_approved": 100.00,
            "notes_from_admin": ":-)",
            }

        form = EventReviewForm(data)
        self.assertTrue(form.is_valid())


class ExpenseFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id, self.event_id = create_event()

    def test_null_event(self):
        data = {
        "amount_claimed": 100.00,
            }

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "proof": SimpleUploadedFile('proof.png', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_blank_event(self):
        data = {
        "event": "",
        "amount_claimed": 100.00,
            }

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "proof": SimpleUploadedFile('proof.png', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_null_amount_claimed(self):
        data = {
        "event": self.event_id,
            }

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "proof": SimpleUploadedFile('proof.png', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertFalse(form.is_valid())

    def test_null_proof(self):
        data = {
        "event": self.event_id,
        "amount_claimed": 100.00,
            }

        form = ExpenseForm(data)
        self.assertFalse(form.is_valid())
        
    def test_full_expected(self):
        data = {
        "event": self.event_id,
        "amount_claimed": 100.00,
            }

        with io.BytesIO(b'000') as fake_file:
            file_data = {
                "proof": SimpleUploadedFile('proof.png', fake_file.read()),
            }

        form = ExpenseForm(data, file_data)
        self.assertTrue(form.is_valid())

class ExpenseReviewFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id, self.event_id, self.expense_id = create_expense()

        def test_funds_from(self):
            for fund in ['C', 'I', 'F']:
                data = {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "funds_from": fund,
                    }

                form = ExpenseReviewForm(data)
                self.assertTrue(form.is_valid())


        def test_expense_status(self):
            for status in ('W', 'S', 'P', 'A', 'F'):
                data = {
                    "status": status,
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
                }

            form = ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())

        def test_full_expected(self):
            data = {
                "status": "V",
                "asked_for_authorization_date": "2016-01-01",
                "send_to_finance_date": "2016-01-01",
                "amount_authorized_for_payment": 100.00,
                "funds_from": "F",
                "notes_from_admin": ":-)",
                }

            form = ExpenseReviewForm(data)
            self.assertTrue(form.is_valid())


class BlogFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id, self.event_id = create_event()

    def test_null_event(self):
        data = {
        "draft_url": "http://software.ac.uk",
            }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_event(self):
        data = {
        "event": "",
        "draft_url": "http://software.ac.uk",
            }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_null_draft_url(self):
        data = {
        "event": self.event_id,
            }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_draft_url(self):
        data = {
        "event": self.event_id,
        "draft_url": "",
            }

        form = BlogForm(data)
        self.assertFalse(form.is_valid())

    def test_full_expected(self):
        data = {
        "event": self.event_id,
        "draft_url": "http://software.ac.uk",
            }

        form = BlogForm(data)
        self.assertTrue(form.is_valid())

class ExpenseReviewFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.fellow_id, self.event_id, self.blog_id = create_blog()

        def test_blog_status(self):
            for status in ('U', 'R', 'L', 'P', 'D', 'O'):
                data = {
                    "status": status,
                    }

                form = BlogReviewForm(data)
                self.assertTrue(form.is_valid())


        def test_minimal_expected(self):
            data = {
                "status": "P",
                "published_url": "http://software.ac.uk",
                }

            form = BlogReviewForm(data)
            self.assertTrue(form.is_valid())

        def test_full_expected(self):
            data = {
                "status": "P",
                "published_url": "http://software.ac.uk",
                "notes_from_admin": ":-)",
                }

            form = BlogReviewForm(data)
            self.assertTrue(form.is_valid())
