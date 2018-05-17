"""Context for template"""
from django.contrib.sites.models import Site
from django.utils import timezone

from constance import config

def site(request):  # pylint: disable=unused-argument
    """Return the site."""
    return {
        'site': Site.objects.get_current()
    }

def organisation(request):  # pylint: disable=unused-argument
    """Return the organisation."""
    return {
        'organisation_name': config.ORGANISATION_NAME,
        'organisation_website': config.ORGANISATION_WEBSITE,
    }

def maintenance(request):  # pylint: disable=unused-argument
    """Return true if default maintancance time."""
    now = timezone.now()

    if now.weekday() == config.MAINTENANCE_DAY and now.hour == config.MAINTENANCE_HOUR:
        return {"is_maintenance_time": True}

    return {"is_maintenance_time": False}
