from datetime import date, timedelta

from django_extensions.management.jobs import DailyJob

from ...models import *
from ...mail import *

class Job(DailyJob):
    help = "Reminder staffs to review one request."

    def execute(self):
        today = date.today()
        days_to_responde = timedelta(0, 0, 3)  # 72 horus
        funds = Fund.objects.filter(
            status__in="UP",
            added__lte=today - days_to_responde
        )
        for fund in funds:
            new_fund_staff_reminder_notification(fund)
