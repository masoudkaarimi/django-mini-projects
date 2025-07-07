import random

from django import template

register = template.Library()


@register.filter(name='random_badge_class')
def random_badge_class(tag):
    badge_classes = ['badge-light', 'badge-success', 'badge-info', 'badge-danger', 'badge-warning']
    return random.choice(badge_classes)
