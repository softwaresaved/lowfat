"""
Send email for some views.
"""
import ast

from constance import config

from html2text import html2text

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template

from .models import *
from .settings import DEFAULT_FROM_EMAIL, SITE_ID

def mail_staffs(subject, message, fail_silently=False, connection=None, html_message=None):
    """Overwrite of Django mail_staffs()"""
    msg = EmailMultiAlternatives(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        ast.literal_eval(config.STAFFS_EMAIL),
        connection=connection,
        reply_to=[config.FELLOWS_MANAGEMENT_EMAIL]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send(fail_silently=fail_silently)

def new_notification(staff_url, email_url, user_email, context, mail):
    if config.STAFF_EMAIL_NOTIFICATION:
        # Email to staff
        context.update({
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        })

        flatemail = FlatPage.objects.get(url=staff_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text(html)
        mail_staffs(
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

        flatemail = FlatPage.objects.get(url=email_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text(html)
        msg = EmailMultiAlternatives(
            flatemail.title,
            plain_text,
            DEFAULT_FROM_EMAIL,
            user_email,
            reply_to=[config.FELLOWS_MANAGEMENT_EMAIL]
        )
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        mail.justification = plain_text
        mail.save()

def new_fund_notification(fund):
    staff_url = "/email/template/fund/staff/"
    email_url = "/email/template/fund/claimant/"
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

    new_notification(staff_url, email_url, user_email, user_context, mail)

def new_expense_notification(expense):
    staff_url = "/email/template/expense/staff/"
    email_url = "/email/template/expense/claimant/"
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


    new_notification(staff_url, email_url, user_email, user_context, mail)

def new_blog_notification(blog):
    staff_url = "/email/template/blog/staff/"
    email_url = "/email/template/blog/claimant/"
    user_email = [blog.author.email]
    if blog.coauthor.all():
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

    new_notification(staff_url, email_url, user_email, context, mail)

def review_notification(email_url, user_email, context, mail, copy_to_staffs=False, copy_to_gatekeeper=False):   # pylint: disable=too-many-arguments
    """Compose the message and send the email."""
    if config.CLAIMANT_EMAIL_NOTIFICATION and email_url is not None:
        # Generate message
        flatemail = FlatPage.objects.get(url=email_url)
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
        msg = EmailMultiAlternatives(
            flatemail.title,
            plain_text,
            mail.sender.email,
            user_email,
            cc=[config.WEBSITE_GATEKEEPER_EMAIL] if copy_to_gatekeeper else None,
            bcc=ast.literal_eval(config.STAFFS_EMAIL) if copy_to_staffs else None,
            reply_to=[config.FELLOWS_MANAGEMENT_EMAIL]
        )
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        # Every email is archived in the database
        mail.save()

def fund_review_notification(message, sender, old, new, copy_to_staffs):
    user_email = [new.claimant.email]
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

    if new.status in ('A', 'R'):
        email_url = "/email/template/fund/claimant/change/"
    elif message:
        email_url = "/email/template/default/"
    else:
        email_url = None

    review_notification(email_url, user_email, context, mail, copy_to_staffs)

def expense_review_notification(message, sender, old, new, copy_to_staffs):
    user_email = [new.fund.claimant.email]

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

    if new.status == 'A':
        email_url = "/email/template/expense/claimant/change/"
    elif message:
        email_url = "/email/template/default/"
    else:
        email_url = None

    review_notification(email_url, user_email, context, mail, copy_to_staffs)

def blog_review_notification(message, sender, old, new, copy_to_staffs):
    user_email = [new.author.email]
    if new.coauthor.all():
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

    if new.status == 'P':
        email_url = "/email/template/blog/claimant/publish/"
        copy_to_gatekeeper = True
    elif new.status == 'G':
        email_url = "/email/template/blog/claimant/proofread/"
        context["WEBSITE_GATEKEEPER"] = config.WEBSITE_GATEKEEPER
        context["WEBSITE_GATEKEEPER_EMAIL"] = config.WEBSITE_GATEKEEPER_EMAIL
        copy_to_gatekeeper = True
    elif message:
        email_url = "/email/template/default/"
        copy_to_gatekeeper = False
    else:
        email_url = None
        copy_to_gatekeeper = False

    review_notification(email_url, user_email, context, mail, copy_to_staffs, copy_to_gatekeeper)

def staff_reminder(request):  # pylint: disable=invalid-name
    if config.STAFF_EMAIL_REMINDER:
        request_type = type(request).__name__.lower()
        staff_url = "/email/template/{}/staff/reminder/".format(
            request_type
        )

        context = {
            request_type: request,
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        }

        flatemail = FlatPage.objects.get(url=staff_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text(html)
        mail_staffs(
            flatemail.title,
            plain_text,
            html_message=html,
            fail_silently=False
        )
