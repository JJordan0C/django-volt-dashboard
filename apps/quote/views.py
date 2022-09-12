import json
from django.shortcuts import get_object_or_404, render

from core.utils import html_to_pdf
from .models import *
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pandas as pd
from django.core import serializers
from locale import setlocale, LC_ALL
# Create your views here.


class TestView(View):
    def get(self, request):
        from .quote_parser import parse_quote
        parse_quote()


class DashboardView(View):
    def get(self, request):
        return render(request, 'home/dashboard.html')


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
            'quote_type_ids': range(104, 116),
            'match_ids': range(504, 604)
        }
        # data = request.POST.get('data')
        dealer = request.user.get_dealer()
        QuoteType = dealer.get_sub_model(Dealer.SUB_MODEL.QUOTE_TYPE)
        Event = dealer.get_sub_model(Dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(Dealer.SUB_MODEL.EVENTQUOTE)

        quote_types = QuoteType.objects.filter(
            id__in=data_example['quote_type_ids'])
        events = Event.objects.filter(id__in=data_example['match_ids'])
        dataframe_data = {e.competition.name: [] for e in events}

        for e in events:
            quotes = tuple(orjson.loads(getattr(e, EventQuote.__name__.lower(
            ) + '_set').get().quote)[qt.id] for qt in quote_types)
            dataframe_data[e.competition.name].append(
                (
                    # e.competition.name, # MANIFESTAZIONE
                    # e.data.strftime("%d/%m/%Y %H:%M"), # DATA
                    e.data.strftime("%a %d/%m %H:%M"),  # DATA
                    e.fast_code,  # FASTCODE
                    e.name,  # AVVENIMENTO
                ) + quotes
            )

        # METHOD 1
        # df = pd.DataFrame(dataframe_data)#.set_index([0,1,2,3])
        # df.index.names=

        # cols = ['MANIFESTAZIONE', 'DATA', 'FASTCODE', 'AVVENIMENTO']
        #tuples = [(x, '') for x in cols] + [(qt.get_super_quote, qt.get_sub_quote) for qt in quote_types]
        # cols = pd.MultiIndex.from_tuples(tuples)
        # df.columns = cols
        # writer = pd.ExcelWriter('goldbet.xlsx', engine='xlsxwriter')
        # df.to_excel(writer, sheet_name='goldbet')

        # # # Auto-adjust columns' width
        # for column in df:
        #     column_width = max(df[column].astype(str).map(len).max(), len(column))
        #     col_idx = df.columns.get_loc(column)
        #     writer.sheets['goldbet'].set_column(col_idx, col_idx, column_width)

        # writer.save()

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
            'data': dataframe_data,
            'columns': cols,
            'dealer_image': str(get_key_from_value(settings.DEALERS, dealer.name)) + '.jpg',
            'col_group_borders_childs': [i for i,v in enumerate(cols) if len(v.sub_columns) > 0]
        }

        return render(request, 'quote/table_to_pdf.html', context=context)
