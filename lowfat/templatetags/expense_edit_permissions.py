from django import template

register = template.Library()


@register.filter
def can_edit_expense(user, expense):
    if user.is_superuser:
        return True
    claimant = getattr(expense.fund, "claimant", None)
    is_fellow_owner = claimant and claimant.user == user

    # Fellow can only edit in these states:
    editable_statuses = {"S", "E"}  # Submitted, Returned to the claimant
    return is_fellow_owner and expense.status in editable_statuses
