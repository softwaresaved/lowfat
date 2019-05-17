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

    def run_requests(self, url, queries, follow=True):
        """Wrapper to run the requests.

        queries = [
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {"foo": "bar"},
            }
        ]"""
        for query in queries:
            if "post_data" in query:
                response = query["user"].post(url, query["post_data"], follow=follow)
            else:
                response = query["user"].get(url, follow=follow)
            self.assertEqual(
                response.status_code,
                query["expect_code"],
                "when {} requested {} {} passing {}".format(
                    query["user"].name,
                    "POST" if "post_data" in query else "GET",
                    url,
                    query["post_data"] if "post_data" in query else None
                )
            )
            if follow is True and response.redirect_chain:
                if "final_url" in query:
                    self.assertEqual(
                        response.redirect_chain[-1][0],
                        query["final_url"],
                        "when {} requested {} {} passing {} it should be redirect".format(
                            query["user"].name,
                            "POST" if "post_data" in query else "GET",
                            url,
                            query["post_data"] if "post_data" in query else None
                        )
                    )
                elif "final_url_regex" in query:
                    self.assertRegex(  # pylint: disable=deprecated-method
                        response.redirect_chain[-1][0],
                        query["final_url_regex"],
                        "when {} requested {} {} passing {} it should be redirect".format(
                            query["user"].name,
                            "POST" if "post_data" in query else "GET",
                            url,
                            query["post_data"] if "post_data" in query else None
                        )
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

        # We don't test the final_url because GitHub redirect will not work locally.
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

        self.run_requests(url, queries, follow=False)

    def test_disconnect(self):
        url = '/disconnect/'

        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": "/",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": "/",
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "final_url": "/",
            },
            ]

        self.run_requests(url, queries)

    def test_my_profile(self):
        url = '/my-profile/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/login/?next=/my-profile/",
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
                "expect_code": 404,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant_details_by_id(self):
        url = '/claimant/{}/'.format(self.claimant_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 404,
            },
            {
                "user": self.claimant_a,
                "expect_code": 404,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 404,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant_details_by_slug(self):
        url = '/claimant/{}/'.format(Claimant.objects.get(id=self.claimant_id).slug)
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
                "expect_code": 200,
                "final_url": "/login/?next=/claimant/",
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

    def test_claimant_promote_view(self):
        url = '/promote/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant_promote(self):
        url = '/fellow/{}/promote'.format(self.claimant_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            ]

        self.run_requests(url, queries)

    def test_claimant_demote(self):
        url = '/fellow/{}/demote'.format(self.claimant_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": "/admin/login/?next={}".format(url),
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
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/review",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/request/\d+/",
            },
            ]

        self.run_requests(url, queries)

    def test_request_review(self):
        url = '/request/{}/review'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/admin/login/\?next=/request/\d+/review",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "status": "A",
                    "ad_status": "V",
                    "grant_heading": "F",
                    "grant": "SSI1",
                    "required_blog_posts": 1,
                    "budget_approved": 100.00,
                },
                "final_url_regex": r"/request/\d+/",
            },
            ]

        self.run_requests(url, queries)

    def test_fund_details(self):
        url = '/fund/{}/'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/fund/\d+/",
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

    def test_request_details(self):
        url = '/request/{}/'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/request/\d+/",
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

    def test_request_reply(self):
        url = '/request/{}/reply/'.format(self.fund_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/request/\d+/reply/",
                "post_data": {"message": "Email body"},
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {"message": "Email body"},
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,
                "post_data": {"message": "Email body"},
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {"message": "Email body"},
            },
            ]

        self.run_requests(url, queries)

    def test_fund(self):
        url = '/fund/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/login/?next=/fund/",
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

    def test_request(self):
        url = '/request/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/login/?next=/request/",
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
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/expense/\d+/review",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/request/\d+/expense/\d+",
            },
            ]

        self.run_requests(url, queries)

    def test_expense_review_relative(self):
        this_expense = Expense.objects.get(id=self.expense_id)
        url = '/fund/{}/expense/{}/review'.format(self.fund_id, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/admin/login/\?next=/fund/\d+/expense/\d+/review",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "status": "S",
                    "asked_for_authorization_date": "2016-01-01",
                    "send_to_finance_date": "2016-01-01",
                    "amount_authorized_for_payment": 100.00,
                    "grant_heading": "F",
                    "grant": "SSI1",
                },
                "final_url_regex": r"/request/\d+/expense/\d+",
            },
            ]

        self.run_requests(url, queries)

    def test_expense_claim_relative(self):
        this_expense = Expense.objects.get(id=self.expense_id)
        url = '/fund/{}/expense/{}/pdf'.format(self.fund_id, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/fund/\d+/expense/\d+/pdf",
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

    def test_expense_details(self):
        url = '/expense/{}/'.format(self.expense_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 404,
            },
            {
                "user": self.claimant_a,
                "expect_code": 404,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,
            },
            {
                "user": self.admin,
                "expect_code": 404,
            },
            ]

        self.run_requests(url, queries)

    def test_expense_details_relative(self):
        this_expense = Expense.objects.get(id=self.expense_id)
        url = '/fund/{}/expense/{}/'.format(self.fund_id, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/fund/\d+/expense/\d+/",
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
                "expect_code": 200,
                "final_url": "/login/?next=/expense/",
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
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                    "status": "P",
                    "title": "Foo",
                    "published_url": "https://www.software.ac.uk/",
                    "tweet_url": "https://twitter.com/FakeUser/status/999999999999999999",
                },
                "final_url_regex": r"/admin/login/\?next=/blog/\d+/review",
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
                "final_url_regex": r"/blog/\d+/",
            },
            ]

        self.run_requests(url, queries)

    def test_blog_details(self):
        url = '/blog/{}/'.format(self.blog_id)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/blog/\d+/",
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
                "expect_code": 200,
                "final_url": "/login/?next=/blog/",
            },
            {
                "user": self.public,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                },
                "final_url": "/login/?next=/blog/",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                },
                "final_url_regex": r"/blog/\d+/",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "post_data": {
                    "draft_url":  "https://www.software.ac.uk/",
                },
                "final_url_regex": r"/blog/\d+/",
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
                },
                "final_url_regex": r"/blog/",
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "author": 1,
                    "draft_url":  "https://www.software.ac.uk/",
                },
                "final_url_regex": r"/blog/\d+/",
            },
            ]

        self.run_requests(url, queries)

    def test_dashboard(self):
        url = '/dashboard/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/login/?next=/dashboard/",
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
                "expect_code": 200,
                "final_url": "/admin/login/?next=/geojson/",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": "/admin/login/?next=/geojson/",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": "/admin/login/?next=/geojson/",
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
