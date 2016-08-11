from django.test import TestCase

from .models import fix_url

class FixURLTest(TestCase):
    def none(self):
        url = None
        expected_url = None

        self.assertTrue(fix_url(url), expected_url)

    def blank(self):
        url = ""
        expected_url = ""

        self.assertTrue(fix_url(url), expected_url)

    def without_protocol(self):
        url = "software.ac.uk"
        expected_url = "http://software.ac.uk"

        self.assertTrue(fix_url(url), expected_url)

    def with_http(self):
        url = "http://software.ac.uk"
        expected_url = "http://software.ac.uk"

        self.assertTrue(fix_url(url), expected_url)

    def with_https(self):
        url = "https://software.ac.uk"
        expected_url = "https://software.ac.uk"

        self.assertTrue(fix_url(url), expected_url)
