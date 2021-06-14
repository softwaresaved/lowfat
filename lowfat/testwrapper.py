"""
Wrapper around tests
"""
import pathlib

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from .models import *

User = get_user_model()

ADMIN_PASSWORD = '123456'
CLAIMED_A_PASSWORD = '123456'
CLAIMED_B_PASSWORD = '123456'

# Define the base directory for lowfat
BASE_DIR = pathlib.Path(__name__).absolute().parent


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

    # Must be able to find a T&Cs otherwise 404
    terms = TermsAndConditions.objects.create(  # pylint: disable=unused-variable
        year=str(timezone.now().year),
        url='Dummy URL'
    )

    # define data for claimant_b
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
        "fellow": True,
    }
    # With claimant_b's image open make and save to the test_db claimant_b
    with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
        data.update({
            "photo": ImageFile(test_image, name="ali-christensen.jpg"),
        })

        claimant_b = Claimant(**data)
        claimant_b.save()

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
        "fellow": True,
    }
    # With claimant_a's image open make and save to the test_db claimant_a
    with open(BASE_DIR.joinpath("upload/photos/ali-christensen.jpg"), 'rb') as test_image:
        data.update({
            "photo": ImageFile(test_image, name="ali-christensen.jpg"),
        })

        claimant_a = Claimant(**data)
        claimant_a.save()
    return claimant_a.id


def create_fund(claimant_id):
    _claimant = Claimant.objects.get(id=claimant_id)

    data = {
        "claimant": _claimant,
        "category": "A",
        "status": "A",
        "title": "Fake",
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
    claimant_id = create_claimant()
    fund_id = create_fund(claimant_id)
    _fund = Fund.objects.get(id=fund_id)

    data = {
        "fund": _fund,
        "amount_claimed": "100.00",
        }

    with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
        data.update({
            "claim": File(fake_file, name="ec1.pdf"),
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
