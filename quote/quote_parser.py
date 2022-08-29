import requests
import orjson
from django.conf import settings
from threading import Thread
from .models import *

def get_data(dealer_id):
    response = requests.get(url=settings.QUOTE_URL.format(dealer_id = dealer_id))
    return orjson.loads(response.content)


def initial_config():
    def to_do(dealer: Dealer):
        print('DIO')
        data = get_data(dealer.id)
        
        quote_types = data['desquote'].replace('|',' - ').split('?')
        qt_list = [dealer.get_sub_model(dealer.SUB_MODEL.QUOTE_TYPES)(name=q) for q in quote_types ]
        for x in qt_list:
            x.save()
        
    all_dealers = Dealer.objects.all()
    
    t_list = [Thread(target=to_do, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
        
    for t in t_list:
        t.join()