from django import template

register = template.Library()


@register.filter
def can_edit_expense(user, expense):
    if user.is_superuser:
        return True
    claimant = getattr(expense.fund, "claimant", None)
    return claimant and user == claimant.user and expense.status == "S"
