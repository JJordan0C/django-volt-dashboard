from django.db import models
from .utils import create_model, create_table

# Create your models here.

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)   

    class Meta:  
        db_table = "dealers"
        
        
for dealer in Dealer.objects.all():
    # Group = type('Group', (models.Model,), {
    #     'id': models.AutoField(primary_key=True) ,
    #     'name': models.CharField(max_length=50, blank=True, null=True)
    # })
    name = f'{dealer.name}Group'
    fields = {
        'id': models.AutoField(primary_key=True) ,
        'name': models.CharField(max_length=50, blank=True, null=True),
        '__str__': lambda self: self.name,
    }
    options = {
        'db_table': name
    }
    globals()[name] = create_model(
        name, 
        fields,
        options=options,
        app_label='apps.quote',
        module='apps.quote.models'
    )
    
    # print(globals()[name])
    # print(Dealer)
    
    # fields = [
    #     ('id', models.AutoField(primary_key=True)) ,
    #     ('name', models.CharField(max_length=50, blank=True, null=True)),
    #     #('__str__', lambda self: self.name),
    # ]
    # create_table(name, fields, options, 'apps.quote')
    
    # from django.db.migrations import CreateModel
    
    # m = CreateModel(name, fields, options, bases=(models.Model,),) 