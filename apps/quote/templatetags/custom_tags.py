import base64
from django import template
from datetime import datetime
from django.conf import settings

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
        
    return ''
    
def is_in_lbi(val):
    return val+1 in lbi

def image(url):
    # from os.path import join
    # url = join(assets_root, base_path, image) 
    url = 'apps' + settings.ASSETS_ROOT + url
    with open(url, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

register.filter('is_today', is_today)
register.simple_tag(append_lbi)
register.simple_tag(image)
register.filter(is_in_lbi)