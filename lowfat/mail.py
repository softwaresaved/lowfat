"""
Send email for some views.
"""
import ast

from constance import config

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import Context, Template

from .models import *
from .settings import DEFAULT_FROM_EMAIL, SITE_ID

def mail_admins(subject, message, fail_silently=False, connection=None, html_message=None):
    """Overwrite of Django mail_admins()"""
    admins = ast.literal_eval(config.STAFFS_EMAIL)  # XXX This is unsecure

    send_mail(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        admins,
        fail_silently=fail_silently,
        connection=connection,
        html_message=html_message
    )

def new_notification(admin_url, admin_context, user_url, user_email, user_context):
    admin_context.update({
        "protocol": "https",
        "site": Site.objects.get(id=SITE_ID),
        "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
    })
    user_context.update({
        "protocol": "https",
        "site": Site.objects.get(id=SITE_ID),
        "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
    })

    if config.STAFF_EMAIL_NOTIFICATION:
        # Email to admin
        flatemail = FlatPage.objects.get(url=admin_url)
        template = Template(flatemail.content)
        context = Context(admin_context)
        mail_admins(
            flatemail.title,
            template.render(context),
            fail_silently=False
        )

    if config.CLAIMANT_EMAIL_NOTIFICATION:
        # Email to claimant
        flatemail = FlatPage.objects.get(url=user_url)
        template = Template(flatemail.content)
        context = Context(user_context)
        send_mail(
            flatemail.title,
            template.render(context),
            DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False
        )

def new_fund_notification(fund):
    admin_url = "/email/template/fund/admin/"
    admin_context = {
        "fund": fund,
    }

    user_url = "/email/template/fund/claimant/"
    user_context = {
        "fund": fund,
    }
    user_email = fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def new_expense_notification(expense):
    admin_url = "/email/template/expense/admin/"
    admin_context = {
        "expense": expense,
    }

    user_url = "/email/template/expense/claimant/"
    user_context = {
        "expense": expense,
    }
    user_email = expense.fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def new_blog_notification(blog):
    admin_url = "/email/template/blog/admin/"
    admin_context = {
        "blog": blog,
    }

    user_url = "/email/template/blog/claimant/"
    user_context = {
        "blog": blog,
    }
    user_email = blog.fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def review_notification(mail, old, new, url):
    """Compose the message and send the email."""
    if config.CLAIMANT_EMAIL_NOTIFICATION:
        # Generate message
        flatemail = FlatPage.objects.get(url=url)
        template = Template(flatemail.content)
        context = Context({
            "old": old,
            "new": new,
            "notes": mail.justification,
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        })
        mail.justification = template.render(context)

        # Email to claimant
        send_mail(
            flatemail.title,
            mail.justification,
            mail.sender.email,
            [mail.receiver.email],
            fail_silently=False
        )

def fund_review_notification(message, sender, old, new):
    if new.status in ('A', 'R'):
        mail = FundSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.claimant,
                "fund": new,
            }
        )

        review_notification(mail, old, new, "/email/template/fund/claimant/change/")

        if message:
            mail.save()

def expense_review_notification(message, sender, old, new):
    if new.status == 'A':
        mail = ExpenseSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.fund.claimant,
                "expense": new,
            }
        )

        review_notification(mail, old, new, "/email/template/expense/claimant/change/")

        if message:
            mail.save()

def blog_review_notification(message, sender, old, new):
    if new.status == 'P':
        mail = BlogSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.author,
                "blog": new,
            }
        )

        review_notification(mail, old, new, "/email/template/blog/claimant/change/")

        if message:
            mail.save()
