from django.db import models
from apps.quote.models import Dealer
from apps.quote.utils import create_table


for dealer in Dealer.objects.all():
    # Group = type('Group', (models.Model,), {
    #     'id': models.AutoField(primary_key=True) ,
    #     'name': models.CharField(max_length=50, blank=True, null=True)
    # })
    name = f'{dealer.name}Group'
    options = {
        'db_table': name
    }
    
    fields = [
        ('id', models.AutoField(primary_key=True)) ,
        ('name', models.CharField(max_length=50, blank=True, null=True)),
        #('__str__', lambda self: self.name),
    ]
    create_table(name, fields, options, 'apps.quote')