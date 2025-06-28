from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()

    for key in list(query.keys()):
        if query[key] == '' or query[key] == 'default':
            query.pop(key)

    for k, v in kwargs.items():
        if v is None or v == '' or v == 'default':
            query.pop(k, None)
        else:
            query[k] = v
    return query.urlencode()

