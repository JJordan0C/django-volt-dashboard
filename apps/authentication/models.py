# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from core.task import scheduler
from phonenumber_field.modelfields import PhoneNumberField

from apps.quote.models import Dealer

# Create your models here.
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    s_name = models.TextField(max_length=320)
    address = models.TextField(max_length=320)
    s_tel = PhoneNumberField()
    
    
class User(AbstractUser):
   dealer_id = models.IntegerField(null=True)
   shop = models.ForeignKey(to=Shop, null=True, on_delete=models.CASCADE)
   
   def get_dealer(self):
       if self.dealer_id and not self.is_superuser:
           return Dealer.get(id=self.dealer_id)
       
       return Dealer.all()[0]