import unittest

from django.test import Client
from django.contrib.auth.models import User

ADMIN_PASSWORD = '123456'

class SimpleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        User.objects.create_superuser('admin',
                                      'admin@fake.software.ac.uk',
                                      ADMIN_PASSWORD)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        self.admin = Client()
        self.admin.login(username='admin',
                         password=ADMIN_PASSWORD)
                              
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_sign_in(self):
        response = self.client.get('/sign_in/')
        self.assertEqual(response.status_code, 200)

    def test_fellow(self):
        response = self.client.get('/fellow/')
        self.assertEqual(response.status_code, 302)  # Need admin permission
                         
        response = self.admin.get('/fellow/')
        self.assertEqual(response.status_code, 200)

    def test_event(self):
        response = self.client.get('/event/')
        self.assertEqual(response.status_code, 200)

    def test_expense(self):
        response = self.client.get('/expense/')
        self.assertEqual(response.status_code, 200)
