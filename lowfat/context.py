"""Context processors to add data to template context."""
from django.contrib.sites.models import Site
from django.utils import timezone

from constance import config


def site(request):  # pylint: disable=unused-argument
    # type: (...) -> dict
    """Return the site."""
    return {
        'site': Site.objects.get_current()
    }


def organisation(request):  # pylint: disable=unused-argument
    # type: (...) -> dict
    """Return the organisation."""
    return {
        'organisation_name': config.ORGANISATION_NAME,
        'organisation_website': config.ORGANISATION_WEBSITE,
    }


def maintenance(request):  # pylint: disable=unused-argument
    # type: (...) -> dict
    """Return whether current time is within scheduled maintenance period."""
    now = timezone.now()

    return {
        'is_maintenance_time': now.weekday() == config.MAINTENANCE_DAY and now.hour == config.MAINTENANCE_HOUR
    }
