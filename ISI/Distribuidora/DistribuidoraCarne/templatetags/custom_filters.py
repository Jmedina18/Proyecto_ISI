from django import template
from django.utils.safestring import mark_safe
import locale

register = template.Library()

@register.filter(name='get_item')
def get_item(lst, i):
    return lst[i]

@register.filter(name='formato_numero')
def formato_numero(value):
    # Formatear el número con comas para separar miles
    try:
        if value:
            locale.setlocale(locale.LC_ALL, '')
            return mark_safe(locale.format_string("%.2f", float(value), grouping=True))
        else:
            return value
    except (ValueError, TypeError):
        return value

@register.filter(name='multiplica_numero')
def multiplica_numero(value, arg):
    """
    Multiplica el valor por el argumento y devuelve el resultado.
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
from django import template
from django.utils.safestring import mark_safe
import locale

register = template.Library()

@register.filter(name='get_item')
def get_item(lst, i):
    return lst[i]

@register.filter(name='formato_numero')
def formato_numero(value):
    # Formatear el número con comas para separar miles
    try:
        if value:
            locale.setlocale(locale.LC_ALL, '')
            return mark_safe(locale.format_string("%.2f", float(value), grouping=True))
        else:
            return value
    except (ValueError, TypeError):
        return value

@register.filter(name='multiplica_numero')
def multiplica_numero(value, arg):
    """
    Multiplica el valor por el argumento y devuelve el resultado.
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
