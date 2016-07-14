from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .models import Fellow, Event

class FellowTestCase(TestCase):
    def setUp(self):
        fellows = (
                {
                    "forenames": "A",
                    "surname": "C",
                    "email": "a.c@mail.com",
                    "phone": "+441111111111",
                    "gender": "M",
                    "home_location": "London",
                    "photo": SimpleUploadedFile('a_c.jpg', ''),
                    "research_area": "L391",
                    "affiliation": "King's College",
                    "funding": "Self-funded",
                    "work_description": "Work",
                    "website": "",
                    "website_feed": "",
                    "orcid": "",
                    "github": "",
                    "gitlab": "",
                    "twitter": "",
                    "facebook": "",
                },
                )

        for fellow in fellows:
            Fellow.objects.create(**fellow)

    def test_setUp(self):
        pass


class EventTestCase(TestCase):
    def setUp(self):
        fellow = FellowTestCase()
        fellow.setUp()

        events = (
                {
                    "fellow": Fellow.objects.get(id=1),
                    "category": "O",
                    "name": "Test 1",
                    "url": "test1.com",
                    "location": "UK",
                    "start_date": "2016-05-16",
                    "end_date": "2016-05-18",
                    "budget_request_travel": "300.00",
                    "budget_request_attendance_fees": "0.00",
                    "budget_request_subsistence_cost": "0.00",
                    "budget_request_venue_hire": "0.00",
                    "budget_request_catering": "0.00",
                    "budget_request_others": "0.00",
                    "budget_approved": "0.00",
                    "justification": ":-)",
                    "additional_info": "",
                },
                )
        for event in events:
            Event.objects.create(**event)

    def test_setUp(self):
        pass
