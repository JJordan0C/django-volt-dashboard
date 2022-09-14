import json
from django.shortcuts import get_object_or_404, render

from core.utils import  generate_pdf
from .models import *
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pandas as pd
from django.core import serializers
from locale import setlocale, LC_ALL
from threading import Thread
from datetime import datetime
# Create your views here.


class TestView(View):
    def get(self, request):
        from .quote_parser import parse_quote
        parse_quote()


class DashboardView(View):
    def get(self, request):
        dealer = request.user.get_dealer()
        
        context = {
            'dealer': dealer
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

    def get(self, request):
        
        setlocale(LC_ALL, "it_IT")
        
        data_example = {
            #'quote_type_ids': range(150, 167),
            'quote_type_ids': range(104, 121),
            'match_ids': range(504, 704)
        }
        # data = request.POST.get('data')
        dealer = request.user.get_dealer()
        QuoteType = dealer.get_sub_model(Dealer.SUB_MODEL.QUOTE_TYPE)
        Event = dealer.get_sub_model(Dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(Dealer.SUB_MODEL.EVENTQUOTE)

        quote_types = QuoteType.objects.filter(
            id__in=data_example['quote_type_ids'])
        events = Event.objects.filter(id__in=data_example['match_ids'])
        tables = [events[x:x+70] for x in range(0, len(events),70)] # max 70 rows for each table
        dataframe_data = [{e.competition.name: [] for e in t_events} for t_events in tables]
        
        def generate_table(t_events, index):
            for e in t_events:
                quotes = tuple(orjson.loads(getattr(e, EventQuote.__name__.lower(
                ) + '_set').get().quote)[qt.id] for qt in quote_types)
                dataframe_data[index][e.competition.name].append(
                    (
                        # e.competition.name, # MANIFESTAZIONE
                        # e.data.strftime("%d/%m/%Y %H:%M"), # DATA
                        e.data.strftime("%a %d/%m %H:%M"),  # DATA
                        e.fast_code,  # FASTCODE
                        e.name,  # AVVENIMENTO
                    ) + quotes
                )
                
        threads = [Thread(target=generate_table, args=[t_events, ind]) for ind, t_events in enumerate(tables)]
        [t.start() for t in threads]

        # METHOD 2
        class Column:
            def __init__(self, name: str, sub_columns: list = []):
                self.name = name
                self.sub_columns = sub_columns

            def __str__(self):
                return self.name + ' ' + ','.join(self.sub_columns)

        cols = [
            Column('MANIFESTAZIONE'),
            Column('DATA'),
            Column('CODE'),
            Column('AVVENIMENTO')
        ]
        #cols += [Column(qt.get_super_quote.upper(), qt.get_sub_quote.upper()) for qt in quote_types]
        to_add = {qt.get_super_quote.upper(): [] for qt in quote_types}
        [to_add[qt.get_super_quote.upper()].append(qt.get_sub_quote.upper())
         for qt in quote_types]
        cols += [Column(key, val) for key, val in to_add.items()]
        context = {
            'tables_data': dataframe_data,
            'columns': cols,
            'dealer_image': str(get_key_from_value(settings.DEALERS, dealer.name)) + '.jpg',
            'col_group_borders_childs': [i for i,v in enumerate(cols) if len(v.sub_columns) > 0],
            'date_label': datetime.now().strftime('Aggiornamento di %A %d %B %Y alle ore %H:%M:%S')
        }
        [t.join() for t in threads]
        #return render(request, 'quote/table_to_pdf.html', context=context)
        return generate_pdf('quote/table_to_pdf.html', context)
