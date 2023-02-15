"""
Tests use the django testing tools and are run through tox.
The configuration of tox can be found in the file 'tox.ini'.
Users, claimants, funds and blogs for testing are created using functions in 'testwrapper.py'.
test_urls.py tests each of the urls from the perspective of the public, claimants and admin.
"""

from django.test import Client, TestCase

from . import (
    models,
    testwrapper,
)


class URLTest(TestCase):
    def setUp(self):
        """Creates the users, claimants, funds and blogs using the functions from testwrapper.py.
        Sets up the test client to use as a dummy web browser for public, claimant_a, claimant_b, and admin.
        """
        # Create the users, claimants, funds and blogs then get a dictionary contain the test data
        self.claimant_test_data = testwrapper.create_all()

        # Every test needs a client.
        self.public = Client()
        self.public.name = 'public'

        self.claimant_a = Client()
        self.claimant_a.login(
            username='claimant-a',
            password=testwrapper.CLAIMED_A_PASSWORD
        )
        self.claimant_a.name = 'claimant-a'
        # unpack outputs of create_all here for ease of use later
        self.claimant_id_a = self.claimant_test_data[self.claimant_a.name]['claimant_id']
        self.fund_id_a = self.claimant_test_data[self.claimant_a.name]['fund_id']
        self.expense_id_a = self.claimant_test_data[self.claimant_a.name]['expense_id']
        self.blog_id_a = self.claimant_test_data[self.claimant_a.name]['blog_id']

        self.claimant_b = Client()
        self.claimant_b.login(
            username='claimant-b',
            password=testwrapper.CLAIMED_B_PASSWORD
        )
        self.claimant_b.name = 'claimant-b'
        # unpack outputs of create_all here for ease of use later
        self.claimant_id_b = self.claimant_test_data[self.claimant_b.name]['claimant_id']
        self.fund_id_b = self.claimant_test_data[self.claimant_b.name]['fund_id']
        self.expense_id_b = self.claimant_test_data[self.claimant_b.name]['expense_id']
        self.blog_id_b = self.claimant_test_data[self.claimant_b.name]['blog_id']

        self.admin = Client()
        self.admin.login(
            username='admin',
            password=testwrapper.ADMIN_PASSWORD
        )
        self.admin.name = 'admin'

    def run_requests(self, url, queries, follow=True):
        """Wrapper to run the requests.

        queries = [
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {"foo": bar"},
            }
        ]
        """
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
        """Tests login for public, claimants and admin.
        """
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
        """Test login with github.
        """
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
        """Tests url when user is disconnected (uses LogoutView)."""
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
        """Tests view of own profile."""
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
        """Tests claimant detail page."""
        url = '/claimant/{}/'.format(self.claimant_id_a)
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
        """Tests claimant details page when accessed by slug."""
        url = '/claimant/{}/'.format(
            models.Claimant.objects.get(id=self.claimant_id_a).slug
        )

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
        """Tests page for creating claimants."""
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
        """Tests page for promoting claimants to fellows.
        """
        url = '/promote/'
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_claimant_promote(self):
        """Tests page showing that a claimant has been promoted to a fellow."""
        url = '/fellow/{}/promote/'.format(self.claimant_id_a)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_claimant_demote(self):
        """Tests page for a fellow demoted to a claimant."""
        url = '/fellow/{}/demote/'.format(self.claimant_id_a)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": f"/admin/login/?next={url}",
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_fund_review(self):
        """Tests funding request review page."""
        url = '/fund/{}/review/'.format(self.fund_id_a)
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
        """Tests funding request review page."""
        url = '/request/{}/review/'.format(self.fund_id_a)
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
        """Tests page showing details of a funding request."""
        url = '/fund/{}/'.format(self.fund_id_a)
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
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's fund
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_request_details(self):
        """Tests page showing details of a funding request."""
        url = '/request/{}/'.format(self.fund_id_a)
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
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's fund
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_fund(self):
        """Tests funding request form page."""
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
        """Tests funding request form page."""
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

    def test_request_with_id(self):
        """Tests page of funding request detail for own funding request and the funding request of another claimant."""
        url = '/request/{}/'.format(self.fund_id_a)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": "/login/?next=/request/{}/".format(self.fund_id_a),
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,   # A 404 is expected as claimant_b is trying to access claimant_a's fund
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_expense_review_relative(self):
        """Tests review of expense claim."""
        this_expense = models.Expense.objects.get(id=self.expense_id_a)
        url = '/fund/{}/expense/{}/review/'.format(self.fund_id_a, this_expense.relative_number)
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
        """Tests link to uploaded expense claim document."""
        this_expense = models.Expense.objects.get(id=self.expense_id_a)
        url = '/fund/{}/expense/{}/claim/'.format(self.fund_id_a, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/fund/\d+/expense/\d+/claim",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's expense
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_expense_receipts_relative(self):
        """Tests link to uploaded receipts."""
        this_expense = models.Expense.objects.get(id=self.expense_id_a)
        url = '/fund/{}/expense/{}/receipts/'.format(self.fund_id_a, this_expense.relative_number)
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url_regex": r"/login/\?next=/fund/\d+/expense/\d+/receipts",
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
            },
            {
                "user": self.claimant_b,
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's expense
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_expense_details_relative(self):
        """Tests page showing detail of an expense claim."""
        this_expense = models.Expense.objects.get(id=self.expense_id_a)
        url = '/fund/{}/expense/{}/'.format(self.fund_id_a, this_expense.relative_number)
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
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's expense
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_expense(self):
        """Tests page showing expense claim form."""
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
        """Tests blog review page."""
        url = '/blog/{}/review/'.format(self.blog_id_a)
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
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
        """Tests page showing detail about blog post."""
        url = '/blog/{}/'.format(self.blog_id_a)
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
                "expect_code": 404,  # A 404 is expected as claimant_b is trying to access claimant_a's blog
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_blog(self):
        """Tests page showing form for submitting a blog post draft."""
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
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
                    "draft_url": "https://www.software.ac.uk/",
                },
                "final_url_regex": r"/blog/",
            },
            {
                "user": self.admin,
                "expect_code": 200,
                "post_data": {
                    "author": 1,
                    "draft_url": "https://www.software.ac.uk/",
                },
                "final_url_regex": r"/blog/\d+/",
            },
        ]

        self.run_requests(url, queries)

    def test_dashboard(self):
        """Tests dashboard."""
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
        """Tests geojson url."""
        url = '/geojson/'
        final_url = "/admin/login/?next=/geojson/"
        queries = [
            {
                "user": self.public,
                "expect_code": 200,
                "final_url": final_url,
            },
            {
                "user": self.claimant_a,
                "expect_code": 200,
                "final_url": final_url,
            },
            {
                "user": self.claimant_b,
                "expect_code": 200,
                "final_url": final_url,
            },
            {
                "user": self.admin,
                "expect_code": 200,
            },
        ]

        self.run_requests(url, queries)

    def test_index(self):
        """Tests index page."""
        url = '/index/'

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
