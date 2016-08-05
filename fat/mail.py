"""
Send email for some views.
"""
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse

from .settings import DEFAULT_FROM_EMAIL

def reverse_full(*args, **kargs):
    """Return the full address using Django reverse."""
    # FIXME Avoid hard code the domain.
    return 'http://dev.fat.software.ac.uk{}'.format(reverse(*args, **kargs))

def new_event_notification(event):
    # Email to admin
    mail_admins("New event request",
            "Please review {}.".format(
                reverse_full("event_review", args=[event.id])),
                fail_silently=False,
            )

    # Email to user
    send_mail('Your event request was received',
            'You can check the information of your event at {}.'.format(
                reverse_full("event_detail", args=[event.id])),
            DEFAULT_FROM_EMAIL,
            [event.fellow.email],
            fail_silently=False
            )

def new_expense_notification(expense):
    # Email to admin
    mail_admins("New expense submited",
            "Please process {}.".format(
                reverse_full("expense_review", args=[expense.id])),
                fail_silently=False,
            )

    # Email to user
    send_mail('Your new expense claim was received',
            'You can check the information of your expense claim at {}.'.format(
                reverse_full("expense_claim", args=[expense.id])),
            DEFAULT_FROM_EMAIL,
            [expense.event.fellow.email],
            fail_silently=False
            )

def new_blog_notification(blog):
    # Email to admin
    mail_admins("New blog request",
            "Please review {}.".format(
                reverse_full("event_review", args=[blog.id])),
                fail_silently=False,
            )

    # Email to user
    send_mail('Your new blog post was received',
            'You can check the information of your event at {}.'.format(
                reverse_full("event_detail", args=[blog.id])),
            DEFAULT_FROM_EMAIL,
            [blog.event.fellow.email],
            fail_silently=False
            )
