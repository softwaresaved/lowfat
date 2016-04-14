from django.test import TestCase
from .models import Event

class EventTestCase(TestCase):
    def setUp(self):
        events = (
                {
                    "fellow": 1,
                    "category": "O",
                    "name": "CW16",
                    "url": "http://www.software.ac.uk/cw16",
                    "location": "Edinburgh",
                    "start_date": "2016-03-18",
                    "end_date": "2016-03-20",
                    "budget_request_travel": 100.00,
                    "budget_request_attendance_fees": 50.00,
                    "budget_request_subsistence_cost": 50.00,
                    "budget_request_venue_hire": 0.00,
                    "budget_request_catering": 0.00,
                    "budget_request_others": 0.00,
                    "justification": "Collaborate.",
                },
                )
        for event in events:
            Event.objects.create(**event)
