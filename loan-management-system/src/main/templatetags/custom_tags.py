from django import template
from django.utils.translation import get_language_info, gettext_lazy as _
from django.utils.formats import localize

from core.utils import to_jalali

register = template.Library()


@register.filter("get_language_fullname")
def get_language_fullname(language_code):
    try:
        return _(get_language_info(language_code)['name'])
    except KeyError:
        return language_code


@register.filter(name="intcomma_local")
def intcomma_local(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value  # Value is not an int; return it unchanged
    return localize("{:,}".format(value))


@register.filter(name='to_jalali')
def to_jalali_filter(input_date, output_format='%Y-%m-%d'):
    return to_jalali(input_date, output_format)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_admin')
def is_admin(user):
    return user.is_staff or user.is_superuser
