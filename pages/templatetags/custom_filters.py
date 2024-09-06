from django import template
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='truncate_lines')
def truncate_lines(value, lines):
    if not isinstance(value, str):
        return value

    soup = BeautifulSoup(value, "html.parser")
    lines = int(lines)
    lines_list = soup.prettify().split('\n')
    truncated_lines = lines_list[:lines]

    # بازسازی HTML با خطوط برش خورده
    truncated_html = '\n'.join(truncated_lines)

    return mark_safe(truncated_html)  # استفاده از mark_safe

@register.filter(name='multiply')
def multiply(value, arg):
    # Convert values to Decimal if they are not already
    if isinstance(value, (int, float)):
        value = Decimal(value)
    if isinstance(arg, (int, float)):
        arg = Decimal(arg)
    return value * arg
