import datetime

from django.core.management.base import BaseCommand

from lowfat.models import Claimant, Fund, Expense

class Command(BaseCommand):
    help = "CW19 funding request"

    def handle(self, *args, **options):
        for claimant in Claimant.objects.filter(
                application_year=2019
        ):
            candidate = Claimant.objects.get(
                email=claimant.email,
                application_year=2018
            )
            for fund in Fund.objects.filter(
                    claimant=claimant
            ):
                print("Transfering {} from {} to {} ...".format(
                    fund,
                    claimant,
                    candidate
                    )
                )
                fund.claimant = candidate
                fund.save()
                print("Transfer complete.")
            print("Removing {} ...".format(claimant))
            claimant.delete()
            print("Remove successful.")
