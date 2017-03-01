"""Context for template"""
from django.utils import timezone

def maintenance(request):
    """Return true if default maintancance time."""
    now = timezone.now()

    if now.weekday() == 4 and now.hour == 9:
        return {"is_maintenance_time": True}

    return {"is_maintenance_time": False}
