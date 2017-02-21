"""
Send email for some views.
"""
from constance import config
from django.contrib.flatpages.models import FlatPage
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse
from django.template import Context, Template

from .models import *
from .settings import DEFAULT_FROM_EMAIL

def reverse_full(*args, **kargs):
    """Return the full address using Django reverse."""
    # FIXME Avoid hard code the domain.
    return '{}{}'.format(
        config.DOMAIN,
        reverse(*args, **kargs)
    )

def new_notification(admin_url, admin_context, user_url, user_email, user_context):
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
        "link": reverse_full("fund_review", args=[fund.id]),
    }

    user_url = "/email/template/fund/claimant/"
    user_context = {
        "fund": fund,
        "link": reverse_full("fund_detail", args=[fund.id]),
    }
    user_email = fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def new_expense_notification(expense):
    admin_url = "/email/template/expense/admin/"
    admin_context = {
        "expense": expense,
        "link": reverse_full("expense_review", args=[expense.id]),
    }

    user_url = "/email/template/expense/claimant/"
    user_context = {
        "expense": expense,
        "link": reverse_full("expense_detail", args=[expense.id]),
    }
    user_email = expense.fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def new_blog_notification(blog):
    admin_url = "/email/template/blog/admin/"
    admin_context = {
        "blog": blog,
        "link": reverse_full("blog_review", args=[blog.id]),
    }

    user_url = "/email/template/blog/claimant/"
    user_context = {
        "blog": blog,
        "link": reverse_full("blog_detail", args=[blog.id]),
    }
    user_email = blog.fund.claimant.email

    new_notification(admin_url, admin_context, user_url, user_email, user_context)

def review_notification(mail, old, new, url):
    if config.CLAIMANT_EMAIL_NOTIFICATION:
        # Email to claimant
        flatemail = FlatPage.objects.get(url=url)
        template = Template(flatemail.content)
        context = Context({
            "old": old,
            "new": new,
            "new_message": mail.justification,
        })
        send_mail(
            flatemail.title,
            template.render(context),
            mail.sender.email,
            [mail.receiver.email],
            fail_silently=False
        )

def fund_review_notification(message, sender, old, new):
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
    mail = BlogSentMail(
        **{
            "justification": message,
            "sender": sender,
            "receiver": new.fund.claimant,
            "blog": new,
        }
    )

    review_notification(mail, old, new, "/email/template/blog/claimant/change/")

    if message:
        mail.save()
