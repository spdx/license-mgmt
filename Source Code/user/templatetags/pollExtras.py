from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def trim(value):
    trimmedString = value.strip("('")
    value = trimmedString.strip("'),")
    return value