from django.shortcuts import render
from .models import *
from django.views import View

# Create your views here.
        
class TestView(View):
    def get(self, request):
        from .quote_parser import parse_quote
        parse_quote()
        
        
class DashboardView(View):
    def get(self, request):
        print('io')
        return render(request, 'home/dashboard.html')
    

class QuoteView(View):
    
    def get(self, request):
        
        dealer = request.user.get_dealer()
        if request.user.is_superuser:
            dealer = dealer[0]
        
        competitions = dealer.get_sub_model(dealer.SUB_MODELS.COMPETITION).objects.all()
        quote_types = dealer.get_sub_model(dealer.SUB_MODELS.QUOTE_TYPE).objects.all()
        
        context = {
            'competitions' : competitions,
            'quote_types' : quote_types
        }
                
        return render(request, 'quote/generate_quote.html', context=context)