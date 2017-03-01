"""Context for template"""
from django.utils import timezone

from constance import config

def maintenance(request):  # pylint: disable=unused-argument
    """Return true if default maintancance time."""
    now = timezone.now()

    if now.weekday() == config.MAINTENANCE_DAY and now.hour == config.MAINTENANCE_HOUR:
        return {"is_maintenance_time": True}

    return {"is_maintenance_time": False}
