import requests
import orjson
from django.conf import settings
from threading import Thread
from .models import Dealer
from datetime import datetime
import numpy as np

def get_data(dealer_id):
    response = requests.get(url=settings.QUOTE_URL.format(dealer_id = dealer_id))
    return orjson.loads(response.content)

# @register_job(scheduler,'interval', seconds=2, replace_existing=True, coalesce=False)
def initial_config():
    
    def save_quote_types(dealer: Dealer):
        data = get_data(dealer.id)
        
        quote_types = data['desquote'].split('?')[:-1]
        
        sub_model = dealer.get_sub_model(dealer.SUB_MODEL.QUOTE_TYPE)
        
        if sub_model.objects.all().count() < len(quote_types):
            
            qt_list = [sub_model(name=q) for q in quote_types ]
            print(sub_model, len(qt_list))
            sub_model.objects.bulk_create(qt_list, ignore_conflicts=True)
    
    all_dealers = Dealer.all()
    
    t_list = [Thread(target=save_quote_types, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
        
    # for t in t_list:
    #     t.join()
    

def parse_quote():
    
    def parse(dealer: Dealer):
        data = get_data(dealer.id)
        competitions_list, events_list, events_quote_list = [[] for x in range(3)]
        
        Competition = dealer.get_sub_model(dealer.SUB_MODEL.COMPETITION)
        Event = dealer.get_sub_model(dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(dealer.SUB_MODEL.EVENTQUOTE)
        # QuoteType = dealer.get_sub_model(dealer.SUB_MODEL.QUOTE_TYPE)
        
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
                'competition_name' : c_kwargs['name'],
                'data' : datetime.strptime(event['eventopenDate'], '%Y-%m-%dT%H:%M:%S'),
                'avv' : avv,
            }
            
            if fastcode:
                e_kwargs['fast_code'] = fastcode
            
            # q_kwargs = [{'quote' : q, 'event_name': e_kwargs['name']} for q in event['quote']]
            q_kwargs = {
                'quote' : orjson.dumps(event['quote']).decode("utf-8"), 
                'event_name': e_kwargs['name']
            }
            
            if c_kwargs not in competitions_list:
                competitions_list.append(Competition(**c_kwargs))
                
            if e_kwargs not in events_list:
                events_list.append(e_kwargs)
                
            if q_kwargs not in events_quote_list:
                events_quote_list.append(q_kwargs)
                
        #objects = Competition.objects.bulk_update_or_create(competitions_list, ['name', 'pal'], match_field='name', yield_objects=True)
        Competition.objects.bulk_update_or_create(competitions_list, ['name', 'pal'], match_field='name')
        print('Competizioni aggiunte e aggiornate')
            #events_list[ind]['competition_id'] = comp.id
        for e in events_list:
            e['competition'] = Competition.objects.get(name=e['competition_name'])
            del e['competition_name']
            
        Event.objects.bulk_update_or_create([Event(**e) for e in events_list], events_list[0].keys(), match_field='name')
        print('Eventi aggiunti e aggiornati')
        
        for q in events_quote_list:
            q['event'] = Event.objects.get(name=q['event_name'])
            del q['event_name']
            
        EventQuote.objects.bulk_update_or_create([EventQuote(**q) for q in events_quote_list], events_quote_list[0].keys(), match_field='event_id')
        # quote_types = QuoteType.objects.all()
        # def save_quotes(l_eq_list):
        #     for eq_kwargs in l_eq_list:
        #         event_name = Event.objects.get(name=eq_kwargs[0]['event_name'])
        #         print(event_name, len(eq_kwargs))
        #         for ind, qt in enumerate(quote_types):
        #             eq_kwargs[ind]['event'] = event_name
        #             eq_kwargs[ind]['qt'] = qt
        #             del eq_kwargs[ind]['event_name']
        #         EventQuote.objects.bulk_update_or_create([EventQuote(**eq) for eq in eq_kwargs], eq_kwargs[0].keys(), match_field='id')
            
        # t_list = [Thread(target=save_quotes, args=[x]) for x in np.array_split(events_quote_list, 4)]
        # [t.start() for t in t_list]
        # [t.join() for t in t_list]
        
        print('Quote Eventi aggiunte e aggiornate')
            
        
    print('yeee parsing')
    all_dealers = Dealer.all()
    t_list = [Thread(target=parse, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()