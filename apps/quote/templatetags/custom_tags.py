from django import template
from datetime import datetime

register = template.Library()

def is_today(event_tuple:tuple):
    return datetime.strptime(event_tuple[0], "%a %d/%m - %H:%M").date() == datetime.today().date()

register.filter('is_today', is_today)