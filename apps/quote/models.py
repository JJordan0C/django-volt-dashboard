from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
import re
from django.conf import settings
from core.utils import get_key_from_value
from json import JSONDecoder, JSONEncoder
import orjson

def simple_plural(word):
    if word[-1] == "y":
        word = word[:-1] + 'ies'
    else:
        word += 's'
    return word

### BASE MODELS

def base_meta(obj):
    split_class_name = re.findall('[a-zA-Z][^A-Z]*', obj.__name__)
    db_table = split_class_name[0] + "_" + "_".join([ simple_plural(x) for x in split_class_name[1:]])
    return type('Meta', (), { 'db_table': db_table})

class BaseQuoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def dealer_name(self):
        return re.findall('[a-zA-Z][^A-Z]*', self.__class__.__name__)[0]
    
    @property
    def dealer(self):
        return Dealer.get(id=get_key_from_value(settings.DEALERS, self.dealer_name))
        
    class Meta:
        abstract=True
    

class BaseQuoteType(BaseQuoteModel):
    name = models.CharField(max_length=50, unique=True, blank=True)
    
    class Meta:
        abstract = True
        
    def has_sub_quotes(self):
        return '|' in self.name
    
    def get_sub_quotes(self):
        if not self.has_sub_quotes():
            return None
        to_search = self.get_super_quote() + '|'
        return self.__class__.objects.filter(name__contains=to_search)
    
    def get_sub_quote(self):
        return self.name.split('|')[-1]
    
    def get_super_quote(self):
        return self.name.split('|')[0]
    

class BaseCompetition(BaseQuoteModel):
    name = models.CharField(max_length=50, unique=True)
    pal = models.IntegerField()
    
    class Meta:
        abstract = True

    @property
    def matches(self):
        return self.dealer.get_sub_model(Dealer.SUB_MODEL.EVENT).objects.filter(competition_id=self.id) 

class BaseForeignKey(models.ForeignKey):
    
    def __init__(self, dynamic=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BaseEvent(BaseQuoteModel):
    name = models.CharField(max_length=50, unique=True)
    data = models.DateTimeField(null=True)
    fast_code = models.IntegerField(null=True)
    avv = models.IntegerField(null=True)
    
    # @property
    # def get_competition_id(self):
    #     return models.ForeignKey(to=f'quote.{self.dealer_name}Competition', on_delete=models.deletion.CASCADE)
    
    # def save(self, *args, **kwargs):
    #     self.competition_id = self.get_competition_id
    #     print(self.competition_id)
    #     super(BaseQuoteModel, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True
        # fields = ('name', 'data', 'fast_code', 'avv', 'competition_id')

class BaseEventQuote(BaseQuoteModel):
    
    #quote = models.FloatField(null=True)
    quote = models.JSONField(null=True)
    
    # @classmethod
    # @property
    # def event_id(self):
    #     return models.ForeignKey(to=f'quote.{self.dealer_name}Event', on_delete=models.deletion.CASCADE)
    
    # # @classmethod
    # @property
    # def qt_id(self):
    #     return models.ForeignKey(to=f'quote.{self.dealer_name}QuoteType', on_delete=models.deletion.CASCADE)
    
    class Meta:
        abstract = True
    
###  MODELS

class Dealer:
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    class SUB_MODEL:
        QUOTE_TYPE = 'QuoteType'
        COMPETITION = 'Competition'
        EVENT = 'Event'
        EVENTQUOTE = 'EventQuote'

    # class Meta:
    #     # db_table = "dealers"
    #     abstract = True
        
    def all():
        return [Dealer(id=id, name=name) for id, name in settings.DEALERS.items()]
    
    def get(id:int = None, name:str = None):
        r = None
        if id:
            r = Dealer(id=id, name=settings.DEALERS[id]) if id in settings.DEALERS.keys() else None
        
        if name:
            id = get_key_from_value(settings.DEALERS, name)
            r = Dealer(id=id, name=name) if id in settings.DEALERS.keys() else None
            
        return r

    def get_sub_model(self, sub_model):
        return globals()[f'{self.name}{sub_model}']




class GoldbetQuoteType(BaseQuoteType):
    pass

class GoldbetCompetition(BaseCompetition):
    pass

class GoldbetEvent(BaseEvent):
    pass

class GoldbetEventQuote(BaseEventQuote):
    pass

class SnaiQuoteType(BaseQuoteType):
    pass

class SnaiCompetition(BaseCompetition):
    pass

class SnaiEvent(BaseEvent):
    pass

class SnaiEventQuote(BaseEventQuote):
    pass

class EurobetQuoteType(BaseQuoteType):
    pass

class EurobetCompetition(BaseCompetition):
    pass

class EurobetEvent(BaseEvent):
    pass

class EurobetEventQuote(BaseEventQuote):
    pass

class PlanetcoinQuoteType(BaseQuoteType):
    pass

class PlanetcoinCompetition(BaseCompetition):
    pass

class PlanetcoinEvent(BaseEvent):
    pass

class PlanetcoinEventQuote(BaseEventQuote):
    pass

class StanleybetQuoteType(BaseQuoteType):
    pass

class StanleybetCompetition(BaseCompetition):
    pass

class StanleybetEvent(BaseEvent):
    pass

class StanleybetEventQuote(BaseEventQuote):
    pass



for d in Dealer.all():
    EventQuote = d.get_sub_model('EventQuote')
    Event = d.get_sub_model('Event')
    EventQuote.add_to_class('event', models.ForeignKey(to=f'quote.{d.name}Event', on_delete=models.deletion.CASCADE))
    # EventQuote.add_to_class('qt', models.ForeignKey(to=f'quote.{d.name}QuoteType', on_delete=models.deletion.CASCADE))
    Event.add_to_class('competition', models.ForeignKey(to=f'quote.{d.name}Competition', on_delete=models.deletion.CASCADE))