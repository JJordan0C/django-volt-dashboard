from django.shortcuts import render
from django_apscheduler.jobstores import register_job
from core.task import scheduler
from .models import *
from django.views import View

# Create your views here.
        
class TestView(View):
    def get(self, request):
        return True