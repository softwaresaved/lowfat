"""
Send email for some views.
"""
import ast

from constance import config

from html2text import html2text

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

def new_notification(admin_url, user_url, user_email, context, mail):
    if config.STAFF_EMAIL_NOTIFICATION:
        # Email to admin
        context.update({
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        })

        flatemail = FlatPage.objects.get(url=admin_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text(html)
        mail_admins(
            flatemail.title,
            plain_text,
            html_message=html,
            fail_silently=False
        )

    if config.CLAIMANT_EMAIL_NOTIFICATION:
        # Email to claimant
        context.update({
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        })

        flatemail = FlatPage.objects.get(url=user_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text(html)
        send_mail(
            flatemail.title,
            plain_text,
            DEFAULT_FROM_EMAIL,
            user_email,
            html_message=html,
            fail_silently=False
        )
        mail.justification = plain_text
        mail.save()

def new_fund_notification(fund):
    admin_url = "/email/template/fund/admin/"
    user_url = "/email/template/fund/claimant/"
    user_email = [fund.claimant.email]
    user_context = {
        "fund": fund,
    }
    mail = FundSentMail(
        **{
            "justification": "",
            "sender": None,
            "receiver": fund.claimant,
            "fund": fund,
        }
    )

    new_notification(admin_url, user_url, user_email, user_context, mail)

def new_expense_notification(expense):
    admin_url = "/email/template/expense/admin/"
    user_url = "/email/template/expense/claimant/"
    user_email = [expense.fund.claimant.email]
    user_context = {
        "expense": expense,
    }
    mail = ExpenseSentMail(
        **{
            "justification": "",
            "sender": None,
            "receiver": expense.fund.claimant,
            "expense": expense,
        }
    )


    new_notification(admin_url, user_url, user_email, user_context, mail)

def new_blog_notification(blog):
    admin_url = "/email/template/blog/admin/"
    user_url = "/email/template/blog/claimant/"
    user_email = [blog.author.email]
    if len(blog.coauthor.all()) > 0:
        user_email.extend([author.email for author in blog.coauthor.all()])
    context = {
        "blog": blog,
    }
    mail = BlogSentMail(
        **{
            "justification": "",
            "sender": None,
            "receiver": blog.author,
            "blog": blog,
        }
    )

    new_notification(admin_url, user_url, user_email, context, mail)

def review_notification(user_url, user_email, context, mail):
    """Compose the message and send the email."""
    if config.CLAIMANT_EMAIL_NOTIFICATION:
        # Generate message
        flatemail = FlatPage.objects.get(url=user_url)
        template = Template(flatemail.content)
        context.update({
            "notes": mail.justification,
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        })
        context = Context(context)
        html = template.render(context)
        plain_text = html2text(html)
        mail.justification = plain_text

        # Email to claimant
        send_mail(
            flatemail.title,
            plain_text,
            mail.sender.email,
            user_email,
            html_message=html,
            fail_silently=False
        )
        # Every email is archived in the database
        mail.save()

def fund_review_notification(message, sender, old, new):
    if new.status in ('A', 'R'):
        user_email = [new.claimant.email]
        user_url = "/email/template/fund/claimant/change/"
        context = {
            "old": old,
            "new": new,
            }
        mail = FundSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.claimant,
                "fund": new,
            }
        )

        review_notification(user_url, user_email, context, mail)

def expense_review_notification(message, sender, old, new):
    if new.status == 'A':
        user_email = [new.fund.claimant.email]
        user_url = "/email/template/expense/claimant/change/"
        context = {
            "old": old,
            "new": new,
            }
        mail = ExpenseSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.fund.claimant,
                "expense": new,
            }
        )

        review_notification(user_url, user_email, context, mail)

def blog_review_notification(message, sender, old, new):
    if new.status == 'P':
        user_email = [new.author.email]
        user_url = "/email/template/blog/claimant/change/"
        if len(new.coauthor.all()) > 0:
            user_email.extend([author.email for author in new.coauthor.all()])
        context = {
            "old": old,
            "new": new,
            }
        mail = BlogSentMail(
            **{
                "justification": message,
                "sender": sender,
                "receiver": new.author,
                "blog": new,
            }
        )

        review_notification(user_url, user_email, context, mail)
