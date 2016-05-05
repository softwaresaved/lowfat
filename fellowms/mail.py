"""
Send email for some views.
"""
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse

FROM = "no-reply@fellows.software.ac.uk"

def event2admin(url_event):
    mail_admins("New event request",
            "Please review {}.".format(url_event),
            fail_silently=False
            )

def event2user(user_email, url_event):
    send_mail('Your new event',
            'You can check the information of your event at {}.'.format(reverse("event_detail", args=[url_event])),
            FROM,
            [user_email],
            fail_silently=False
            )
