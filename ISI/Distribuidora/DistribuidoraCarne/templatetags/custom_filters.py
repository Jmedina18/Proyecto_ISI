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
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

    return mark_safe(locale.format_string("%.2f", float(value), grouping=True))