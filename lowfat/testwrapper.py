"""
Wrapper around tests
"""
import io

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import *

ADMIN_PASSWORD = '123456'
CLAIMED_A_PASSWORD = '123456'
CLAIMED_B_PASSWORD = '123456'

def create_users():
    User.objects.create_superuser(
        'admin',
        'admin@fake.lowfat.software.ac.uk',
        ADMIN_PASSWORD
    )
    User.objects.create_user(
        'claimant-a',
        'a.claimant@fake.lowfat.software.ac.uk',
        CLAIMED_A_PASSWORD
    )
    User.objects.create_user(
        'claimant-b',
        'b.claimant@fake.lowfat.software.ac.uk',
        CLAIMED_B_PASSWORD
    )


def create_claimant():
    create_users()

    data = {
        "user": User.objects.get(username="claimant-b"),
        "forenames": "B",
        "surname": "B",
        "email": "b.b@fake.lowfat.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_country": "GB",
        "home_city": "L",
        "research_area": "Y000",
        "research_area_code": "Y000",
        "affiliation": "College",
        "funding": "Self-funded",
        "work_description": "Work",
        "selected": True,
    }

    with io.BytesIO(b'000') as fake_file:
        data.update({
            "photo": SimpleUploadedFile('b_b.jpg', fake_file.read()),
        })

    claimant = Claimant(**data)
    claimant.save()

    data = {
        "user": User.objects.get(username="claimant-a"),
        "forenames": "A",
        "surname": "A",
        "email": "a.a@fake.lowfat.software.ac.uk",
        "phone": "+441111111111",
        "gender": "M",
        "home_country": "GB",
        "home_city": "L",
        "research_area": "Y000",
        "research_area_code": "Y000",
        "affiliation": "College",
        "funding": "Self-funded",
        "work_description": "Work",
        "selected": True,
    }

    with io.BytesIO(b'000') as fake_file:
        data.update({
            "photo": SimpleUploadedFile('a_a.jpg', fake_file.read()),
        })

    claimant = Claimant(**data)
    claimant.save()
    return claimant.id

def create_fund():
    claimant_id = create_claimant()
    claimant = Claimant.objects.get(id=claimant_id)

    data = {
        "claimant": claimant,
        "category": "A",
        "status": "A",
        "name": "Fake",
        "url": "http://fake.com",
        "country": "GB",
        "city": "L",
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

    fund = Fund(**data)
    fund.save()
    return claimant_id, fund.id

def create_all():
    claimant_id, fund_id = create_fund()
    fund = Fund.objects.get(id=fund_id)

    data = {
        "fund": fund,
        "amount_claimed": "100.00",
        }

    with io.BytesIO(b'000') as fake_file:
        data.update({
            "claim": SimpleUploadedFile('fake-claim.jpg', fake_file.read()),
        })

    expense = Expense(**data)
    expense.save()

    data = {
        "fund": fund,
        "author": fund.claimant,
        "draft_url": "http://software.ac.uk",
        }

    blog = Blog(**data)
    blog.save()

    return claimant_id, fund_id, expense.id, blog.id
