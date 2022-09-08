from django import template
from datetime import datetime

register = template.Library()

def is_today(event_tuple:tuple):
    event_date = datetime.strptime(event_tuple[0], "%a %d/%m %H:%M").replace(year=datetime.today().year).date()
    today_date = datetime.today().date()
    return event_date == today_date

def define(val=None):
  return val

lbi = [] #left border indexes (for columns groups borders)
def append_lbi(val, n_sub_cols):
    if len(lbi) == 0:
        lbi.append(val)
        lbi.append(val+n_sub_cols)
    else:
        lbi.append(lbi[-1]+n_sub_cols)
    
def is_in_lbi(val):
    return val+1 in lbi

register.filter('is_today', is_today)
register.simple_tag(append_lbi)
register.filter(is_in_lbi)