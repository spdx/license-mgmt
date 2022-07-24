from django import template
from django.template.defaultfilters import stringfilter
from user.models import licenseTracking

register = template.Library()

@register.filter
@stringfilter
def trim(value):
    trimmedString = value.strip("('")
    value = trimmedString.strip("'),")
    return value

@register.filter
def dateVal(id, position):
    if position=="first":
        trackingObject = licenseTracking.objects.filter(license_id = id).order_by("date")[0]
    else:
        trackingObject = licenseTracking.objects.filter(license_id = id).order_by("-date")[0]
    return trackingObject.date