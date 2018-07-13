from datetime import datetime

from constance import config

from django_extensions.management.jobs import DailyJob

from ...models import Fund, Expense, Blog
from ...mail import staff_reminder, staff_follow_up

class Job(DailyJob):
    help = "Reminder staffs to review one request."

    def execute(self):
        print("""Running {}

config.DAYS_TO_ANSWER_BACK = {}""".format(
    __file__,
    config.DAYS_TO_ANSWER_BACK
))

        today = datetime.now()
        all_unprocessed_requests = [
            Fund.objects.filter(
                status__in="U"  # For Unprocessed
            ),
            Expense.objects.filter(
                status__in="S"  # For Submitted
            ),
            Blog.objects.filter(
                status__in="U"  # For "Waiting for triage"
            ),
        ]
        for requests in all_unprocessed_requests:
            for request in requests:
                if today.day == request.added.day:
                    print("Skipping notification for {} because request was submit today.".format(
                        request
                    ))
                    continue

                datetime_after_request = today - request.added
                days_before_notification = datetime_after_request.days % config.DAYS_TO_ANSWER_BACK
                if days_before_notification == 0:
                    staff_reminder(request)
                else:
                    print("Skipping notification for {}. Notification in {} days.".format(
                        request,
                        days_before_notification
                    ))

        if config.STAFF_EMAIL_FOLLOW_UP and today.weekday() == config.FOLLOW_UP_DAY:
            all_processing_requests = [
                Fund.objects.filter(
                    status__in="P"  # For Processing
                ),
                Expense.objects.filter(
                    status__in="P"  # For Processing
                ),
                Blog.objects.filter(
                    status__in="RCGL"  # For "Waiting to be reviewed", "Reviewing loop", "Waiting to be proofread", "Waiting to be published"
                ),
            ]
            staff_follow_up(all_unprocessed_requests)
        else:
            print("Today is not Skipping notification for {}. Notification in {} days.".format(
                        request,
                        days_before_notification
                    ))
