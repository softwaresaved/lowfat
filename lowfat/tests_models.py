from django.test import TestCase

from .models import Claimant, fix_url

class FixURLTest(TestCase):
    def test_none(self):
        url = None
        expected_url = None

        self.assertEqual(fix_url(url), expected_url)

    def test_blank(self):
        url = ""
        expected_url = ""

        self.assertEqual(fix_url(url), expected_url)

    def test_without_protocol(self):
        url = "software.ac.uk"
        expected_url = "http://software.ac.uk"

        self.assertEqual(fix_url(url), expected_url)

    def test_with_http(self):
        url = "http://software.ac.uk"
        expected_url = "http://software.ac.uk"

        self.assertEqual(fix_url(url), expected_url)

    def test_with_https(self):
        url = "https://software.ac.uk"
        expected_url = "https://software.ac.uk"

        self.assertEqual(fix_url(url), expected_url)


class ClaimantSlugTest(TestCase):
    def test_same_name(self):
        claimant1 = Claimant.objects.create(
            forenames='First Person',
            surname='Test',
            home_city='Testville',
            phone=0
        )

        claimant2 = Claimant.objects.create(
            forenames='Second Person',
            surname='Test',
            home_city='Testville',
            phone=0
        )

        self.assertNotEqual(claimant1.slug, claimant2.slug)
