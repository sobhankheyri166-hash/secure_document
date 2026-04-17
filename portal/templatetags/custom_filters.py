from django import template

register = template.Library()

@register.filter
def is_str(value):
    return isinstance(value,str)