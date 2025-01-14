import orjson
from django.shortcuts import get_object_or_404, render

from core.utils import  generate_pdf, get_pdf_quote_types, localize_datetime
from .models import *
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pandas as pd
from django.core import serializers
from locale import setlocale, LC_ALL
from threading import Thread
from datetime import datetime, timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.authentication.models import User
from django.db.models import Q
from .top_competitions import top
# Create your views here.



class DashboardView(View):
    def get(self, request):
        dealer = request.user.get_dealer()
        users = User.objects.filter(~Q(is_superuser=False)).count()
        context = {
            'dealer': dealer,
            'users': users
        }
        return render(request, 'home/dashboard.html', context=context)


class IndexView(View):
    def get(self, request):
        return HttpResponseRedirect('dashboard')


class QuoteView(View):

    def get(self, request):

        dealer = request.user.get_dealer()

        competitions = dealer.get_sub_model(
            Dealer.SUB_MODEL.COMPETITION).objects.all()
        quote_types = dealer.get_sub_model(
            Dealer.SUB_MODEL.QUOTE_TYPE).objects.all()

        context = {
            'competitions': competitions,
            'quote_types': quote_types,
            'dealer': dealer
        }

        return render(request, 'quote/generate_quote.html', context=context)

    def post(self, request):
        type = request.POST.get('type')
        if type == 'get_matches':
            Competition = request.user.get_dealer().get_sub_model(Dealer.SUB_MODEL.COMPETITION)
            matches = []
            for c in Competition.objects.filter(id__in=request.POST.getlist('competition_ids[]')):
                matches.append([{
                    'id': e.id,
                    'name': e.name,
                    'competition': e.competition.name
                } for e in c.matches])
            return JsonResponse(matches, safe=False)
            
            
class QuoteToPDFView(View):
    
    # method_decorator(cache_page(60 * 60))
    def post(self, request):
        setlocale(LC_ALL, "it_IT.UTF-8")
        
        # data = {
        #     #'quote_type_ids': range(150, 167),
        #     'quote_type_ids': range(104, 121),
        #     'match_ids': '*',
        #     'order_by': 'date', # date, top, country(A-Z)
        #     'date_range_from': localize_datetime(datetime.today().replace(hour=0, minute=1)),
        #     'date_range_to': localize_datetime(datetime.today().replace(hour=0, minute=1) + timedelta(days=5)),
        # }
        
        dealer = request.user.get_dealer()
        QuoteType = dealer.get_sub_model(Dealer.SUB_MODEL.QUOTE_TYPE)
        Event = dealer.get_sub_model(Dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(Dealer.SUB_MODEL.EVENTQUOTE)
        
        body = orjson.loads(request.body)
        data = {
            'champs_ids':body.get('champs_ids'),
            'quote_type_ids': settings.PDF_QUOTE_TYPES[dealer.id],
            'order_by': body.get('order_by'),
            'date_range_from': localize_datetime(datetime.strptime(body.get('date_range_from'), '%d/%m/%Y, %H:%M')), 
            'date_range_to': localize_datetime(datetime.strptime(body.get('date_range_to'), '%d/%m/%Y, %H:%M')),
        }
        
        # data = {
        #     #'quote_type_ids': range(150, 167),
        #     'quote_type_ids': settings.PDF_QUOTE_TYPES[dealer.id],
        #     'match_ids': request.POST.get('match_ids').split(','),
        #     'order_by': request.POST.get('order_by'),
        #     'date_range_from': localize_datetime(datetime.strptime(request.POST.get('date_range_from'), '%d/%m/%Y, %H:%M')), 
        #     'date_range_to': localize_datetime(datetime.strptime(request.POST.get('date_range_to'), '%d/%m/%Y, %H:%M')),
        #     'view_type': request.POST.get('view_type')
        # }

        # quote_types = QuoteType.objects.filter(
        #     id__in=data['quote_type_ids'])
        quote_types = get_pdf_quote_types(QuoteType)
        
        import time 
        start = time.time()
        
        events = Event.objects.filter(competition__id__in=data['champs_ids'], data__range=[data['date_range_from'], data['date_range_to']])
        
        if events.count() == 0:
            return render(request, 'quote/table_to_pdf.html', context={'err': 'Nessun Evento nelle date selezionate'})
        
        if data['order_by'] == 'date':
            events = events.order_by('data')
            
        if data['order_by'] == 'country':
            events = events.order_by('competition__name')
            
        if data['order_by'] == 'top':
            events = [e for t in top[dealer.id] for e in events if e.competition.name == t]
        end = time.time()
        print('CALCOLO EVENTI', (end-start))
        
        tables = [events[x:x+74] for x in range(0, len(events),74)] # max 76 rows for each table
        dataframe_data = [{e.competition.name: [] for e in t_events} for t_events in tables]
        # if data['order_by'] != 'date':
        #     dataframe_data = [{e.competition.name: [] for e in t_events} for t_events in tables]
        # else:
            # dataframe_data = [{e.competition.name + f'C{i}': [] for i,e in enumerate(t_events)} for t_events in tables]
            
        
        today = datetime.today()
        start = localize_datetime(today.replace(hour=0, minute=1))
        end = localize_datetime(today.replace(hour=9, minute=0) + timedelta(days=1))
        
        def generate_table(t_events, index):
            for i, e in enumerate(t_events):
                # quotes = ()
                # for qt in quote_types:
                #     a = getattr(e, EventQuote.__name__.lower() + '_set').get().quote
                #     try:
                #         quotes = quotes + tuple(orjson.loads(a)[qt.id])
                #     except:
                #         print(qt.id, qt.name, 'io vado male')
                
                # raise Exception('dio')
                try:
                    quotes = tuple(orjson.loads(getattr(e, EventQuote.__name__.lower()
                    + '_set').get().quote)[qt.id-1] for qt in quote_types)
                except:
                    continue
                
                if dealer.id == 9:
                    fast_code = str(e.fast_code)[::-1] if start <= e.data <= end else e.fast_code
                else:
                    fast_code = '{}-{}'.format(e.competition.pal, e.avv)
                
                dataframe_data[index][e.competition.name].append(
                    (
                        # e.competition.name, # MANIFESTAZIONE
                        # e.data.strftime("%d/%m/%Y %H:%M"), # DATA
                        e.data.strftime("%a %d/%m %H:%M"),  # DATA
                        fast_code,  # FASTCODE
                        e.name,  # AVVENIMENTO
                    ) + quotes
                )
        
        start = time.time()      
        threads = [Thread(target=generate_table, args=[t_events, ind]) for ind, t_events in enumerate(tables)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        end = time.time()
        print('GENERAZIONE TABELLE', (end-start))

        # METHOD 2
        class Column:
            def __init__(self, name: str, sub_columns: list = []):
                self.name = name
                self.sub_columns = sub_columns

            def __str__(self):
                return self.name + ' ' + ','.join(self.sub_columns)
            
        start = time.time() 
        cols = [
            Column('MANIFESTAZIONE'),
            Column('DATA'),
            Column('CODE') if dealer.id == 9 else Column('PAL-AVV'),
            Column('AVVENIMENTO')
        ]
        #cols += [Column(qt.get_super_quote.upper(), qt.get_sub_quote.upper()) for qt in quote_types]
        to_add = {qt.get_super_quote.upper(): [] for qt in quote_types}
        [to_add[qt.get_super_quote.upper()].append(qt.get_sub_quote.upper())
         for qt in quote_types]
        cols += [Column(key, val) for key, val in to_add.items()]
        end = time.time()
        print('GENERAZIONE COLONNE', (end-start))
        
        context = {
            'tables_data': dataframe_data,
            'columns': cols,
            'dealer_images':['{}_{}.png'.format(dealer.id, i) for i in range(1,4)] if dealer.name == "Goldbet" else [str(dealer.id) + '.png'],
            'col_group_borders_childs': [i for i,v in enumerate(cols) if len(v.sub_columns) > 0],
            'date_label': datetime.now().strftime('Aggiornamento di %A %d %B %Y alle ore %H:%M:%S'),
            'days': (data['date_range_to']-data['date_range_from']).days
        }
        filename = 'Quote_{}_{}.pdf'.format(dealer.name, today.strftime('%Y-%m-%d'))
            # res = render(request, 'quote/table_to_pdf.html', context=context)
            
        return generate_pdf('quote/table_to_pdf.html', context, filename)

