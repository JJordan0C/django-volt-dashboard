import pytz
from re import sub
import requests
import orjson
from django.conf import settings
from threading import Thread

from core.utils import localize_datetime
from .models import Dealer
from datetime import datetime, timezone
import numpy as np
import os

def get_data(dealer_id):
    response = requests.get(url=settings.QUOTE_URL.format(dealer_id = dealer_id))
    return orjson.loads(response.content)

# @register_job(scheduler,'interval', seconds=2, replace_existing=True, coalesce=False)
def initial_config():
    
    def save_quote_types(dealer: Dealer):
        data = get_data(dealer.id)
        
        # Alt + 21
        data['desquote'] = sub('\?(?!\|)', '§', data['desquote'])
        
        quote_types = data['desquote'].split('§')[:-1]
        
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
            
            if dealer.id != 13:
                if dealer.id == 9:
                    pal, avv = param_split[1], param_split[2]  
                else:
                    pal, avv = param_split[0], param_split[1]  
            else: 
                pal, avv = param_split[-2], param_split[-3]
            
            fastcode = param_split[0] if len(param_split) == 3 else None
            
            c_kwargs = {
                'name' : event['compet'],
                'pal' : pal
            }
            
            e_kwargs = {
                'name' : event['eventname'],
                # 'competition_id' : None, #c.id,
                'competition_name' : c_kwargs['name'],
                'data' : localize_datetime(datetime.strptime(event['eventopenDate'], '%Y-%m-%dT%H:%M:%S')), 
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
        # Competition.objects.bulk_update_or_create(competitions_list, ['name', 'pal'], match_field='name',)
        Competition.objects.bulk_create(competitions_list, ignore_conflicts = True)
        print('Competizioni aggiunte e aggiornate')
            #events_list[ind]['competition_id'] = comp.id
            
        for e in events_list:
            e['competition'] = Competition.objects.get(name=e['competition_name'])
            del e['competition_name']
            
        # Event.objects.bulk_update_or_create([Event(**e) for e in events_list], events_list[0].keys(), match_field='id',)
        Event.objects.bulk_create([Event(**e) for e in events_list], ignore_conflicts = True)
        print('Eventi aggiunti e aggiornati')
        
        for q in events_quote_list:
            q['event'] = Event.objects.get(name=q['event_name'])
            del q['event_name']
        EventQuote.objects.bulk_update_or_create([EventQuote(**q) for q in events_quote_list], events_quote_list[0].keys(), match_field='event_id')
        #EventQuote.objects.bulk_create([EventQuote(**{x:y for x,y in q.items() if x != 'event_name'}) for q in events_quote_list], ignore_conflicts = True)
        
        print('Quote Eventi aggiunte e aggiornate')
            
        
    print('yeee parsing')
    all_dealers = Dealer.all()
    t_list = [Thread(target=parse, args=[d]) for d in all_dealers]
    
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
        
        
def remove_old_matches():
    
    def _remove(dealer):
        Event = dealer.get_sub_model(Dealer.SUB_MODEL.EVENT)
        Event.objects.filter(data__lt=localize_datetime(datetime.today())).delete()
    
    t_list = [Thread(target=_remove, args=[d]) for d in Dealer.all()]
    
    [t.start() for t in t_list]
    [t.join() for t in t_list]