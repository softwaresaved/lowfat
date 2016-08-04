import io
import unittest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from .testwrapper import *
from .models import *

ADMIN_PASSWORD = '123456'

class URLTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Insert admin
        create_superuser()
        self.fellow_id, self.event_id, self.expense_id, self.blog_id = create_all()

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

    def test_fellow_details(self):
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

    def test_expense_claims(self):
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
