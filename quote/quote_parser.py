import requests
import orjson
from django.conf import settings
from threading import Thread
from .models import Dealer
from datetime import datetime

def get_data(dealer_id):
    response = requests.get(url=settings.QUOTE_URL.format(dealer_id = dealer_id))
    return orjson.loads(response.content)

# @register_job(scheduler,'interval', seconds=2, replace_existing=True, coalesce=False)
def initial_config():
    
    def save_quote_types(dealer: Dealer):
        data = get_data(dealer.id)
        
        quote_types = data['desquote'].replace('|','&').split('?')[:-1]
        
        sub_model = dealer.get_sub_model(dealer.SUB_MODEL.QUOTE_TYPE)
        
        qt_list = [sub_model(name=q) for q in quote_types ]
        sub_model.objects.bulk_create(qt_list)
    
    all_dealers = Dealer.objects.all()
    t_list = [Thread(target=save_quote_types, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
        
    # for t in t_list:
    #     t.join()
    

def parse_quote():
    
    def parse(dealer: Dealer):
        data = get_data(dealer.id)
        competitions_list = events_list = events_quote_list = []
        
        Competition = dealer.get_sub_model(dealer.SUB_MODEL.COMPETITION)
        Event = dealer.get_sub_model(dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(dealer.SUB_MODEL.EVENTQUOTE)
        
        for event in data['eventi']:
            
            param_split = event['param'].split(':')
            pal, avv = param_split[0], param_split[1]
            fastcode = param_split[2] if len(param_split) == 3 else None
            
            c_kwargs = {
                'name' : event['compet'],
                'pal' : pal
            }
            
            e_kwargs = {
                'name' : event['eventname'],
                # 'competition_id' : None, #c.id,
                # 'competition_name' : c_kwargs['name'],
                'data' : datetime.strptime(event['eventopenDate'], '%Y-%m-%dT%H:%M:%S'),
                'avv' : avv,
                'fastcode' : fastcode
            }
            
            q_kwargs = [{'quote' : q} for q in event['quote']]
            
            if c_kwargs not in competitions_list:
                competitions_list.append(c_kwargs)
                
            if e_kwargs not in events_list:
                events_list.append(e_kwargs)
                
            if q_kwargs not in events_quote_list:
                events_quote_list.append(q_kwargs)
                
        unique_competitions = list(set(competitions_list))
        uc_to_update = [Competition(**c) for c in unique_competitions if Competition.objects.filter(name=c['name']).exists()]
        uc_to_create = [Competition(**c) for c in unique_competitions if Competition(**c) not in uc_to_update]
        
        
            
    
    all_dealers = Dealer.objects.all()
    t_list = [Thread(target=parse, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()