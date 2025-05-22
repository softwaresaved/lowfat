from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from lowfat.models import Claimant, Fund, TermsAndConditions
from datetime import date
from django.utils import timezone

class FundEditAccessTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.terms = TermsAndConditions.objects.create(
        year=str(timezone.now().year),
        url="http://example.com/terms"
)
        # Create test_fellow2 user
        self.fellow = User.objects.create_user(
            username="test_fellow_ui",
            password="Ecs2023!!",
            is_staff=False
        )

        # Claimant profile, first do NOT assign Terms & Conditions and then include it
        self.claimant = Claimant.objects.create(
            user=self.fellow,
            fellow=True,
            forenames="NameTest",
            surname="SurnameFellow",
            email="test_fellow2@example.com",
            phone="123456789",
            home_city="Testville",
            home_country="GB",
        )

        # Create funding request
        self.fund = Fund.objects.create(
            claimant=self.claimant,
            title="Test Event Title Without T&C",
            start_date=date(2025, 5, 10),
            end_date=date(2025, 5, 15),
            budget_request_travel=100,
            budget_request_attendance_fees=50,
            budget_request_subsistence_cost=60,
            budget_request_venue_hire=0,
            budget_request_catering=0,
            budget_request_others=0,
            justification="Test justification",
            success_targeted="Test outcomes",
        )

        self.client = Client()

    def test_edit_blocked_without_terms_and_conditions(self):
        login_success = self.client.login(username="test_fellow_ui", password="12345!!")
        self.assertTrue(login_success)

        response = self.client.get(f"/request/{self.fund.id}/edit/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("terms and conditions", response.content.decode().lower())
