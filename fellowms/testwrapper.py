"""
Wrapper around tests
"""
import io
import unittest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from .models import *

ADMIN_PASSWORD = '123456'

def create_superuser():
    User.objects.create_superuser('admin',
                                  'admin@fake.software.ac.uk',
                                  ADMIN_PASSWORD)

def create_fellow():
    data = {
        "forenames": "C",
        "surname": "A",
        "email": "c.a@fake.fellowms.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_location": "L, UK",
        "research_area": "Y000",
        "research_area_code": "Y000",
        "affiliation": "College",
        "funding": "Self-funded",
        "work_description": "Work",
    }

    with io.BytesIO(b'000') as fake_file:
        data.update({
            "photo": SimpleUploadedFile('a_c.jpg', fake_file.read()),
        })

    fellow = Fellow(**data)
    fellow.save()
    return fellow.id

def create_event():
    fellow_id = create_fellow()
    fellow = Fellow.objects.get(id=fellow_id)
    
    data = {
        "fellow": fellow,
        "category": "A",
        "name": "Fake",
        "url": "http://fake.com",
        "location": "UK",
        "start_date": "2014-02-20",
        "end_date": "2014-02-22",
        "budget_request_travel": "100.00",
        "budget_request_attendance_fees": "0.00",
        "budget_request_subsistence_cost": "0.00",
        "budget_request_venue_hire": "0.00",
        "budget_request_catering": "0.00",
        "budget_request_others": "0.00",
        "justification": ":-)",
        "additional_info": "",
        }

    event = Event(**data)
    event.save()
    return fellow_id, event.id

def create_expense():
    fellow_id, event_id = create_event()
    event = Event.objects.get(id=event_id)

    data = {
        "event": event,
        "amount_claimed": "100.00",
        }

    with io.BytesIO(b'000') as fake_file:
        data.update({
            "proof": SimpleUploadedFile('fake-claim.jpg', fake_file.read()),
        })

    expense = Expense(**data)
    expense.save()
    return fellow_id, event_id, expense.id

def create_blog():
    fellow_id, event_id = create_event()
    event = Event.objects.get(id=event_id)

    data = {
        "event": event,
        "draft_url": "http://google.com/",
        }

    blog = Blog(**data)
    blog.save()
    return fellow_id, event_id, blog.id
