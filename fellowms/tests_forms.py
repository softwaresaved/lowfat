import io
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from .forms import FellowForm

class SimpleTest(unittest.TestCase):
    def test_FellowForm_blank_name(self):
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

    def test_FellowForm_blank_email(self):
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

    def test_FellowForm_blank_phone(self):
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

    def test_FellowForm_blank_location(self):
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

    def test_FellowForm_blank_research_area(self):
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

    def test_FellowForm_blank_research_area_code(self):
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

    def test_FellowForm_blank_affiliation(self):
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


    def test_FellowForm_blank_funding(self):
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

    def test_FellowForm_blank_description(self):
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
        
    def test_FellowForm_null_photo(self):
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

    def test_FellowForm_minimal_expected(self):
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

    def test_FellowForm_full_expected(self):
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
