from django.test import TestCase, Client

from .testwrapper import *
from .models import *


class URLTest(TestCase):
    def setUp(self):
        self.claimant_id, self.fund_id, self.expense_id, self.blog_id = create_all()

        # Every test needs a client.
        self.public = Client()
        self.public.name = 'public'

        self.claimant_a = Client()
        self.claimant_a.login(
            username='claimant-a',
            password=CLAIMED_A_PASSWORD
        )
        self.claimant_a.name = 'claimant-a'

        self.claimant_b = Client()
        self.claimant_b.login(
            username='claimant-b',
            password=CLAIMED_B_PASSWORD
        )
        self.claimant_b.name = 'claimant-b'

        self.admin = Client()
        self.admin.login(
            username='admin',
            password=ADMIN_PASSWORD
        )
        self.admin.name = 'admin'

    def run_requests(self, url, queries):
        """Wrapper to run the requests.

        queries = [
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {"foo": bar"},
            }
        ]"""
        for query in queries:
            if "post_data" in query:
                response = query["user"].post(url, query["post_data"])
            else:
                response = query["user"].get(url)
            self.assertEqual(
                response.status_code,
                query["expect_code"],
                "when requested by {}".format(query["user"].name)
            )

    def test_sign_in(self):
        url = '/login/'

        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_sign_in_with_github(self):
        url = '/login/github/'

        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 302,
            },
            ]

        self.run_requests(url, queries)

    def test_disconnect(self):
        url = '/disconnect/'

        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 302,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant_details(self):
        url = '/claimant/{}/'.format(self.claimant_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant(self):
        url = '/claimant/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_review_relative(self):
        this_expense = Expense.objects.get(id=self.expense_id)
        url = '/fund/{}/expense/{}/review'.format(self.fund_id, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_details(self):
        url = '/expense/{}/'.format(self.expense_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_details_relative(self):
        this_expense = Expense.objects.get(id=self.expense_id)
        url = '/fund/{}/expense/{}/'.format(self.fund_id, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.public,
                "expect_code": 302,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_blog(self):
        url = '/blog/'
        queries = [
            {
                "user": self.public,
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
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
                "expect_code": 302,
            },
            {
                "user": self.claimant_a,
                "expect_code": 302,
            },
            {
                "user": self.claimant_b,
                "expect_code": 302,
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
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)
