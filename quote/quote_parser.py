import requests
import orjson
from django.conf import settings
from threading import Thread
from .models import Dealer


def get_data(dealer_id):
    response = requests.get(url=settings.QUOTE_URL.format(dealer_id = dealer_id))
    return orjson.loads(response.content)

def to_do(dealer: Dealer):
    print('ok ci sono')
    data = get_data(dealer.id)
    
    quote_types = data['desquote'].replace('|',' - ').split('?')
    
    sub_model = dealer.get_sub_model(dealer.SUB_MODEL.QUOTE_TYPES)
    
    qt_list = [sub_model(name=q) for q in quote_types ]
    # for x in qt_list:
    #     x.save()
    sub_model.objects.bulk_create(qt_list)

# @register_job(scheduler,'interval', seconds=2, replace_existing=True, coalesce=False)
def initial_config():
    print('DIO')
    
    all_dealers = Dealer.objects.all()
    to_do(all_dealers[0])
    t_list = [Thread(target=to_do, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
        
    for t in t_list:
        t.join()