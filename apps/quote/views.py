from django.shortcuts import get_object_or_404, render
from .models import *
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
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
        
        competitions = dealer.get_sub_model(Dealer.SUB_MODEL.COMPETITION).objects.all()
        quote_types = dealer.get_sub_model(Dealer.SUB_MODEL.QUOTE_TYPE).objects.all()
        
        context = {
            'competitions' : competitions,
            'quote_types' : quote_types
        }
                
        return render(request, 'quote/generate_quote.html', context=context)
    
    def post(self, request):
        type = request.POST.get('type')
        if type == 'get_matches':
            Competition = request.user.get_dealer().get_sub_model(Dealer.SUB_MODEL.COMPETITION)
            matches = []
            for c in Competition.objects.filter(id__in=request.POST.get('competition_ids')):
                matches.append(c.matches)
                
            return HttpResponse(matches)
            
        
class QuoteToPDFView(View):
    
    def get(self, request):
        data_example = {
            'quote_type_ids': [104,105,106],
            'match_ids': range(504, 507)
        }
        # data = request.POST.get('data')
        dealer = request.user.get_dealer()
        QuoteType = dealer.get_sub_model(Dealer.SUB_MODEL.QUOTE_TYPE)
        Event = dealer.get_sub_model(Dealer.SUB_MODEL.EVENT)
        EventQuote = dealer.get_sub_model(Dealer.SUB_MODEL.EVENTQUOTE)
        
        quote_types = QuoteType.objects.filter(id__in=data_example['quote_type_ids'])
        dataframe_data = []
        
        for e in Event.objects.filter(id__in=data_example['match_ids']):
            #print(type(getattr(e, EventQuote.__name__.lower() + '_set').get().quote.encode()))
            quotes = tuple(orjson.loads(getattr(e, EventQuote.__name__.lower() + '_set').get().quote)[qt.id] for qt in quote_types)
            dataframe_data.append(
                (
                    e.competition.name, # MANIFESTAZIONE
                    e.data.strftime("%d/%m/%Y %H:%M"), # DATA
                    e.fast_code, # FASTCODE
                    e.name, #AVVENIMENTO
                ) + quotes
            )
        print(dataframe_data)
        
        df = pd.DataFrame(dataframe_data)#.set_index([0,1,2,3])
        # df.index.names=
        cols = ['MANIFESTAZIONE', 'DATA', 'FASTCODE', 'AVVENIMENTO']
        print([(x, '') for x in cols] + [(qt.get_super_quote(), qt.get_sub_quote()) for qt in quote_types])
        cols = pd.MultiIndex.from_tuples([(x, '') for x in cols] + [(qt.get_super_quote(), qt.get_sub_quote()) for qt in quote_types])
        df.columns = cols 
        writer = pd.ExcelWriter('goldbet.xlsx') 
        df.to_excel(writer, index=False , sheet_name='goldbet', na_rep='NaN')
        # # Auto-adjust columns' width
        # for column in df:
        #     column_width = max(df[column].astype(str).map(len).max(), len(column))
        #     col_idx = df.columns.get_loc(column)
        #     writer.sheets['goldbet'].set_column(col_idx, col_idx, column_width)

        writer.save()
        return HttpResponse(True)

        
        