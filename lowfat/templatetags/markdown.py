import markdown

from django import template

register = template.Library()  # pylint: disable=invalid-name


@register.filter(name="markdown")
def markdown_filter(value):
    """Markdown to HTML parser."""
    return markdown.markdown(value)
