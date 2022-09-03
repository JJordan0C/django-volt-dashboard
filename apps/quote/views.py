from django.shortcuts import get_object_or_404, render
from .models import *
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
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
            