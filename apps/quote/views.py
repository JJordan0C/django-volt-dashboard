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
        # quote_types = [{
        #         'quote': qt.get_super_quote(),
        #         'sub_quotes': [x.name.split('|')[-1] for x in qt.get_sub_quotes()]
        #     } for qt in QuoteType.objects.filter(id__in=data_example['quote_type_ids'])]
        quote_types = QuoteType.objects.filter(id__in=data_example['quote_type_ids'])
        
        # MANIFESTAZIONE	Data/Ora	CODE	AVVENIMENTO
        
        dataframe_data = []
        
        for e in Event.objects.filter(id__in=data_example['match_ids']):
            quotes = list( getattr(e, EventQuote.__class__.__name__.lower()).get().quote[sub.id] for qt in quote_types for sub in qt.get_sub_quotes())
            print(quotes)
            dataframe_data.append(
                (
                    e.competition.name, # MANIFESTAZIONE
                    e.data, # DATA
                    e.fast_code, # FASTCODE
                    e.name, #AVVENIMENTO
                )
            )
            
        print(dataframe_data)

        
        