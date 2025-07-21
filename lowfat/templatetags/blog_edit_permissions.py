from django import template

register = template.Library()

@register.filter
def can_edit_blog(user, blog):
    # Superusers can always edit
    if user.is_superuser:
        return True

    # Only allow if the user is the author coauthor
    claimant = getattr(blog,'author',None)
    coauthors = getattr(blog,'coauthor',None)
    is_fellow = (
        (claimant and user == claimant.user) or
        (coauthors and coauthors.filter(user=user).exists())
    )

    editable_statuses = {"U", "R", "C"}
    return is_fellow and blog.status in editable_statuses
