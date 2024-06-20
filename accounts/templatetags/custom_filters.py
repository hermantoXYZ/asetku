# custom_filters.py

from django import template

register = template.Library()

@register.filter
def floatformat(value):
    """
    Mengubah nilai float menjadi format Rupiah dengan koma sebagai pemisah desimal.
    """
    return '{:,.2f}'.format(value)

@register.filter
def add_thousand_separator(value):
    """
    Menambahkan pemisah ribuan dengan titik untuk nilai yang lebih besar dari seribu.
    """
    orig = str(value)
    new = ""
    while orig != "":
        if len(orig) <= 3:
            new = orig + new
            break
        else:
            new = "." + orig[-3:] + new
            orig = orig[:-3]
    return new
