from django import template

register = template.Library()
# Canonical mapping of blog status
# Includes both current codes and legacy ones so old rows still display sensibly.
LABELS = {
    # Current codes
    "U": "Waiting for triage",
    "R": "Waiting to be reviewed",
    "C": "Reviewing loop",
    "G": "Waiting to be proofread",
    "P": "Published",
    "K": "Cancelled",
    "D": "Rejected",
    "X": "Removed",

    # Legacy codes – mapped onto the new meanings
    "L": "Waiting to be proofread",  # legacy -> same as G
    "M": "Cancelled",               # legacy -> same as K
    "O": "Cancelled",               # legacy -> same as K
}


@register.filter
def blog_status_label(code: str) -> str:
    """
    Map a blog status code (including legacy codes) to a label.

    """
    return LABELS.get(code, code)
