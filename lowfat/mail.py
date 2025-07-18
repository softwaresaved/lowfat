"""
Send email for some views.
"""
import ast
import smtplib
import logging

from constance import config

from html2text import html2text

from django.contrib import messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.conf import settings
from . import models
from .settings import DEFAULT_FROM_EMAIL, SITE_ID


logger = logging.getLogger(__name__)


def html2text_fix(html):
    """Remove split text in blockquotes."""
    # Workaround until https://github.com/Alir3z4/html2text/pull/179/files is merged.
    return html2text(html).replace("\n\n>", "\n>")


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

        flat_email = FlatPage.objects.get(url=staff_url)
        template = Template(flat_email.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text_fix(html)
        mail_staffs(
            flat_email.title,
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

        flat_email = FlatPage.objects.get(url=email_url)
        template = Template(flat_email.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text_fix(html)
        msg = EmailMultiAlternatives(
            flat_email.title,
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
    mail = models.FundSentMail(
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
    mail = models.ExpenseSentMail(
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
    mail = models.BlogSentMail(
        **{
            "justification": "",
            "sender": None,
            "receiver": blog.author,
            "blog": blog,
        }
    )

    new_notification(staff_url, email_url, user_email, context, mail)


def review_notification(request, email_url, user_email, context, mail, copy_to_staffs=False, copy_to_gatekeeper=False):   # pylint: disable=too-many-arguments
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
        plain_text = html2text_fix(html)
        mail.justification = plain_text

        cc_addresses = [config.FELLOWS_MANAGEMENT_EMAIL]
        if copy_to_gatekeeper:
            cc_addresses.append(config.WEBSITE_GATEKEEPER_EMAIL)

        # Email to claimant
        msg = EmailMultiAlternatives(
            flatemail.title,
            plain_text,
            config.FELLOWS_MANAGEMENT_EMAIL,
            user_email,
            cc=cc_addresses,
            bcc=ast.literal_eval(config.STAFFS_EMAIL) if copy_to_staffs else None
        )
        msg.attach_alternative(html, "text/html")

        try:
            msg.send(fail_silently=False)

        except (ConnectionRefusedError, smtplib.SMTPRecipientsRefused) as exc:
            messages.error(request, "Failed to send notification email.")
            logger.error(exc)

        finally:
            # Every email is archived in the database
            mail.save()


def fund_review_notification(request, message, sender, old, new, copy_to_staffs):
    user_email = [new.claimant.email]
    context = {
        "old": old,
        "new": new,
    }
    mail = models.FundSentMail(
        **{
            "justification": message,
            "sender": sender,
            "receiver": new.claimant,
            "fund": new,
        }
    )

    if new.status in ('A', 'M', 'R'):
        email_url = "/email/template/fund/claimant/change/"
    elif message:
        email_url = "/email/template/default/"
    else:
        email_url = None

    review_notification(request, email_url, user_email, context, mail, copy_to_staffs)


def expense_review_notification(request, message, sender, old, new, copy_to_staffs):
    user_email = [new.fund.claimant.email]

    context = {
        "old": old,
        "new": new,
    }
    mail = models.ExpenseSentMail(
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

    review_notification(request, email_url, user_email, context, mail, copy_to_staffs)


def blog_review_notification(request, message, sender, old, new, copy_to_staffs):
    user_email = [new.author.email]
    if new.coauthor.all():
        user_email.extend([author.email for author in new.coauthor.all()])
    context = {
        "old": old,
        "new": new,
    }
    mail = models.BlogSentMail(
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

    review_notification(request, email_url, user_email, context, mail, copy_to_staffs, copy_to_gatekeeper)


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
        plain_text = html2text_fix(html)
        mail_staffs(
            flatemail.title,
            plain_text,
            html_message=html,
            fail_silently=False
        )


def staff_follow_up(requests):  # pylint: disable=invalid-name
    if config.STAFF_EMAIL_FOLLOW_UP:
        staff_url = "/email/template/staff/follow_up/"

        context = {
            "funds": requests[0],
            "expenses": requests[1],
            "blogs": requests[2],
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
        }

        flatemail = FlatPage.objects.get(url=staff_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text_fix(html)
        mail_staffs(
            flatemail.title,
            plain_text,
            html_message=html,
            fail_silently=False
        )


def claimant_profile_update_notification(claimant):  # pylint: disable=invalid-name
    if config.STAFF_EMAIL_REMINDER:
        staff_url = "/email/template/claimant/staff/update/"
        # need to access the third element of the history because each claimant change is saved twice in
        # claimant_form() once in 'claimant = formset.save()' and once in 'claimant.update_latlon()'
        context = {
            "claimant": claimant,
            "protocol": "https",
            "site": Site.objects.get(id=SITE_ID),
            "FELLOWS_MANAGEMENT_EMAIL": config.FELLOWS_MANAGEMENT_EMAIL,
            "previous_email": claimant.history.all()[2].email
        }

        flatemail = FlatPage.objects.get(url=staff_url)
        template = Template(flatemail.content)
        jinja_context = Context(context)
        html = template.render(jinja_context)
        plain_text = html2text_fix(html)
        mail_staffs(
            flatemail.title,
            plain_text,
            html_message=html,
            fail_silently=False
        )


def notify_finance_if_needed(fund):
    if fund.fund_payment_receiver in ['B', 'C'] or fund.fund_claim_method in ['B', 'C']:
        submitted_on = fund.added.strftime("%Y-%m-%d") if fund.added else "Unknown date"
        user_name = fund.claimant.fullname() if fund.claimant else "Unknown user"
        user_email = fund.claimant.email if fund.claimant and fund.claimant.email else "Unknown email"

        domain = Site.objects.get(id=SITE_ID).domain
        fund_link = f"https://{domain}/fund/{fund.id}/review/"

        subject = f"[ACTION REQUIRED] Possible PO or Employment Status Check for {user_name}"
        body = (
            f"On {submitted_on}, {user_name} submitted a funding request #{fund.id}, which might require a "
            f"Purchase Order or Employment Status Check.\n\n"
            f"Request details: {fund_link}\n\n"
            f"Please investigate and if needed contact {user_name} at {user_email}."
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[config.FUND_FINANCE_EMAIL],
            cc=[config.FUND_FINANCE_EMAIL_CC],
        )
        email.send(fail_silently=False)
