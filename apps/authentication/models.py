# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from core.task import scheduler

from apps.quote.models import Dealer

# Create your models here.
class User(AbstractUser):
   dealer_id = models.IntegerField(null=True)
   
   def get_dealer(self):
       if self.dealer_id and not self.is_superuser:
           return Dealer.get(id=self.dealer_id)
       
       return Dealer.all()[0]