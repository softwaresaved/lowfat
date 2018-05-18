from datetime import date

from django.core.management.base import BaseCommand

from lowfat.models import FormerClaimant, Claimant

class Command(BaseCommand):
    help = "Move Claimant to FormerClaimant after one year of application."

    def handle(self, *args, **options):
        for claimant in Claimant.objects.all():
            if not (claimant.fellow or claimant.collaborator):
                today = date.today()
                if today.year - claimant.application_year >= 1:
                    print("Archiving {} ...".format(claimant))
                    former_claimant = FormerClaimant(
                        gender=claimant.gender,
                        home_country=claimant.home_country,
                        home_city=claimant.home_city,
                        home_lon=claimant.home_lon,
                        home_lat=claimant.home_lat,
                        career_stage_when_apply=claimant.career_stage_when_apply,
                        job_title_when_apply=claimant.job_title_when_apply,
                        research_area=claimant.research_area,
                        funding=claimant.funding,
                        funding_notes=claimant.funding_notes,
                        application_year=claimant.application_year,
                        received_offer=claimant.received_offer,
                        fellow=claimant.fellow,
                        collaborator=claimant.collaborator,
                        is_into_training=claimant.is_into_training,
                        carpentries_instructor=claimant.carpentries_instructor,
                        research_software_engineer=claimant.research_software_engineer,
                        attended_inaugural_meeting=claimant.attended_inaugural_meeting,
                        attended_collaborations_workshop=claimant.attended_collaborations_workshop
                        )
                    former_claimant.save()
                    claimant.delete()
                    print("Sucessfully archived {} ...".format(claimant))
