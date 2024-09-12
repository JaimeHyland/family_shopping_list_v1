from django import template
from utilities.utils import is_adult

register = template.Library()

@register.filter
def is_adult_filter(user):
    return is_adult(user)