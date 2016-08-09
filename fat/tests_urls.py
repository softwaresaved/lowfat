import io

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from .testwrapper import *
from .models import *


class URLTest(TestCase):
    def setUp(self):
        self.fellow_id, self.fund_id, self.expense_id, self.blog_id = create_all()

        # Every test needs a client.
        self.public = Client()
        self.public.name = 'public'

        self.fellow_a = Client()
        self.fellow_a.login(username='fellow-a',
                         password=FELLOW_A_PASSWORD)
        self.fellow_a.name = 'fellow-a'

        self.fellow_b = Client()
        self.fellow_b.login(username='fellow-b',
                         password=FELLOW_B_PASSWORD)
        self.fellow_b.name = 'fellow-b'

        self.admin = Client()
        self.admin.login(username='admin',
                         password=ADMIN_PASSWORD)
        self.admin.name = 'admin'

    def run_requests(self, url, queries):
        """Wrapper to run the requests.

        queries = [
            {
                "user": self.admin,
                "expect_code": 200,
            }
        ]"""
        for query in queries:
            response = query["user"].get(url)
            self.assertEqual(response.status_code,
                             query["expect_code"],
                             "when requested by {}".format(query["user"].name)
            )

    def test_sign_in(self):
        url = '/sign-in/'

        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_fellow_details(self):
        url = '/fellow/{}/'.format(self.fellow_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_fellow(self):
        url = '/fellow/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_fund_review(self):
        url = '/fund/{}/review'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 302,
            },
            {
                "user": self.fellow_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_fund_details(self):
        url = '/fund/{}/'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_fund(self):
        url = '/fund/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_review(self):
        url = '/expense/{}/review'.format(self.expense_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 302,
            },
            {
                "user": self.fellow_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_claims(self):
        url = '/expense/{}/'.format(self.expense_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense(self):
        url = '/expense/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_blog_review(self):
        url = '/blog/{}/review'.format(self.blog_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 302,
            },
            {
                "user": self.fellow_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_blog_details(self):
        url = '/blog/{}/'.format(self.blog_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

    def test_blog(self):
        url = '/blog/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_dashboard(self):
        url = '/dashboard/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_geo(self):
        url = '/geojson/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_index(self):
        url = '/'

        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.fellow_a,
                "expect_code": 200,
            },
            {
                "user": self.fellow_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)
