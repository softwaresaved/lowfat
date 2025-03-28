from django import template

register = template.Library()

@register.filter
def can_edit_fund(user, fund):
    if user.is_superuser:
        return True
    claimant = getattr(fund, "claimant", None)
    return claimant and user == claimant.user and fund.status == "U"
