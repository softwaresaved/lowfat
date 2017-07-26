from datetime import datetime

from constance import config

from django_extensions.management.jobs import DailyJob

from ...models import *
from ...mail import *

class Job(DailyJob):
    help = "Reminder staffs to review one request."

    def execute(self):
        print("""Running {}

config.DAYS_TO_ANSWER_BACK = {}""".format(
    __file__,
    config.DAYS_TO_ANSWER_BACK
))

        today = datetime.now()
        all_requests = [
            Fund.objects.filter(
                status__in="UP"
            ),
            Expense.objects.filter(
                status__in="SC"
            ),
            Blog.objects.filter(
                status__in="UR"
            ),
        ]
        for requests in all_requests:
            for request in requests:
                datetime_after_request = today - request.added
                days_before_notification = datetime_after_request.days % config.DAYS_TO_ANSWER_BACK
                if days_before_notification == 0:
                    staff_reminder(request)
                else:
                    print("Skipping notification for {}. Notification in {} days.".format(
                        request,
                        days_before_notification
                    ))
