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
    """
    Creates three users for testing:
        A superuser: admin
        Two normal users: claimant-a and claimant-b
    """
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


def create_claimants():
    """
    Adds the claimants a/b to the test database with some data.
    Returns:
        We return a tuple containing the ids for claimant a and b
    """
    # Must be able to find a T&Cs otherwise 404
    TermsAndConditions.objects.create(  # pylint: disable=unused-variable
        year=str(timezone.now().year),
        url='Dummy URL'
    )

    # define data for claimant_a
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
    return claimant_a.id, claimant_b.id


def create_fund(*, claimant_id):
    """
    Creates a fund associated with the claimant defined by the argument claimant_id
    Args:
        claimant_id: The id of a claimant stored in the testing database
    """
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

    _fund = Fund(**data)
    _fund.save()
    return _fund


def create_all():
    """
    Create the users, claimants, funds and blogs using the methods defined above.
    Returns:
        claimant_test_data: A dictionary containing claimant_a and claimant_b and associated funds and blogs
    """
    create_users()
    claimant_ids = create_claimants()

    claimant_test_data = {}
    for _claimant_id in claimant_ids:
        _claimant = Claimant.objects.get(id=_claimant_id)
        _fund = create_fund(claimant_id=_claimant_id)

        data = {
            "fund": _fund,
            "amount_claimed": "100.00",
        }

        with open(BASE_DIR.joinpath("upload/expenses/ec1.pdf"), 'rb') as fake_file:
            data.update({
                "claim": File(fake_file, name="ec1.pdf"),
            })

            _expense = Expense(**data)
            _expense.save()

        data = {
            "fund": _fund,
            "author": _fund.claimant,
            "draft_url": "http://software.ac.uk",
        }

        _blog = Blog(**data)
        _blog.save()
        claimant_test_data[f"{_claimant.user.username}"] = {
            'claimant_id': _claimant_id,
            'fund_id': _fund.id,
            'expense_id': _expense.id,
            'blog_id': _blog.id,
        }

    return claimant_test_data
