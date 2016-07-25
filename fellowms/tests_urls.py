import io
import unittest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from .models import *

ADMIN_PASSWORD = '123456'

class URLTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Insert admin
        User.objects.create_superuser('admin',
                                      'admin@fake.software.ac.uk',
                                      ADMIN_PASSWORD)

        # Insert fellow
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
            data.update({
                "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
            })

        fellow = Fellow(**data)
        fellow.save()
        self.fellow_id = fellow.id

        # Insert event
        data = {
            "fellow": fellow,
            "category": "A",
            "name": "Fake",
            "url": "http://fake.com",
            "location": "UK",
            "start_date": "2014-02-20",
            "end_date": "2014-02-22",
            "budget_request_travel": "100.00",
            "budget_request_attendance_fees": "0.00",
            "budget_request_subsistence_cost": "0.00",
            "budget_request_venue_hire": "0.00",
            "budget_request_catering": "0.00",
            "budget_request_others": "0.00",
            "justification": ":-)",
            "additional_info": "",
            }

        event = Event(**data)
        event.save()
        self.event_id = event.id

        # Insert expense
        data = {
            "event": event,
            "amount_claimed": "100.00",
            }

        with io.BytesIO(b'000') as fake_file:
            data.update({
                "proof": SimpleUploadedFile('fake-claim.jpg', fake_file.read()),
            })

        expense = Expense(**data)
        expense.save()
        self.expense_id = expense.id

        # Insert blog
        data = {
            "event": event,
            "draft_url": "http://software.ac.uk/",
            }

        blog = Blog(**data)
        blog.save()
        self.blog_id = blog.id


    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        self.admin = Client()
        self.admin.login(username='admin',
                         password=ADMIN_PASSWORD)


    def test_sign_in(self):
        url = '/sign_in/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fellow_detils(self):
        url = '/fellow/{}/'.format(self.fellow_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fellow(self):
        url = '/fellow/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Need admin permission

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_review(self):
        url = '/event/{}/review'.format(self.event_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Need admin permission

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_details(self):
        url = '/event/{}/'.format(self.event_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event(self):
        url = '/event/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_expense_review(self):
        url = '/expense/{}/review'.format(self.expense_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Need admin permission

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_expense_details(self):
        url = '/expense/{}/'.format(self.expense_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_expense(self):
        url = '/expense/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_review(self):
        url = '/blog/{}/review'.format(self.blog_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Need admin permission

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_details(self):
        url = '/blog/{}/'.format(self.blog_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog(self):
        url = '/blog/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        url = '/dashboard/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_geo(self):
        url = '/dashboard/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        url = '/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin.get(url)
        self.assertEqual(response.status_code, 200)
