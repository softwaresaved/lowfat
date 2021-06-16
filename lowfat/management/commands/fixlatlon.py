import time

from django.core.management.base import BaseCommand

from lowfat.models import Claimant, Fund


class Command(BaseCommand):
    help = "Update latitude and longitude for all Claimant and Fund."

    def handle(self, *args, **options):
        """Nominatim Usage Policy

        - No heavy uses (an absolute maximum of 1 request per second).
        - Provide a valid HTTP Referer or User-Agent identifying the application (stock User-Agents as set by http libraries will not do).
        - Clearly display attribution as suitable for your medium.
        - Data is provided under the ODbL license which requires to share alike (although small extractions are likely to be covered by fair usage / fair dealing).

        Source: https://operations.osmfoundation.org/policies/nominatim/
        """
        for claimant in Claimant.objects.all():
            claimant.update_latlon()
            time.sleep(2)

        for fund in Fund.objects.all():
            fund.update_latlon()
            time.sleep(2)
