from datetime import datetime, timedelta

from constance import config

from django_extensions.management.jobs import DailyJob

from ...models import *
from ...mail import *

class Job(DailyJob):
    help = "Reminder staffs to review one request."

    def execute(self):
        today = datetime.now()
        funds = Fund.objects.filter(
            status="U",
        )
        for fund in funds:
            datetime_after_request = today - fund.added
            days_before_notification = datetime_after_request.days % config.DAYS_TO_ANSWER_BACK
            if days_before_notification == 0:
                new_fund_staff_reminder_notification(fund)
            else:
                print("Skipping notification for {}. Notification in {} days.".format(
                    fund,
                    days_before_notification
                    ))
