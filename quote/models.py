from django.db import models
from .utils import create_model
from django.conf import settings

# Create your models here.

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)   
    
    class SUB_MODEL:
        QUOTE_TYPES = 'QuoteTypes'
        COMPETITIONS = 'Competitions'
        EVENTS = 'Events'
        EVENTQUOTE = 'EventQuote'

    class Meta:  
        db_table = "dealers"
        
    def get_sub_model(self, sub_model):
        return globals()[f'{self.name}{sub_model}']
    

class GoldbetQuoteTypes(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True )

class GoldbetCompetitions(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class GoldbetEvents(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	competition_id = models.ForeignKey(to=f'quote.GoldbetCompetitions', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)

class GoldbetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	event_id = models.ForeignKey(to=f'quote.GoldbetEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.GoldbetQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()

class SnaiQuoteTypes(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True )

class SnaiCompetitions(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class SnaiEvents(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	competition_id = models.ForeignKey(to=f'quote.SnaiCompetitions', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)

class SnaiEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	event_id = models.ForeignKey(to=f'quote.SnaiEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.SnaiQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()

class EurobetQuoteTypes(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True )

class EurobetCompetitions(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class EurobetEvents(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	competition_id = models.ForeignKey(to=f'quote.EurobetCompetitions', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)

class EurobetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	event_id = models.ForeignKey(to=f'quote.EurobetEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.EurobetQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()

class PlanetcoinQuoteTypes(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True )

class PlanetcoinCompetitions(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class PlanetcoinEvents(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	competition_id = models.ForeignKey(to=f'quote.PlanetcoinCompetitions', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)

class PlanetcoinEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	event_id = models.ForeignKey(to=f'quote.PlanetcoinEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.PlanetcoinQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()

class StanleybetQuoteTypes(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True )

class StanleybetCompetitions(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class StanleybetEvents(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	competition_id = models.ForeignKey(to=f'quote.StanleybetCompetitions', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)

class StanleybetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	event_id = models.ForeignKey(to=f'quote.StanleybetEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.StanleybetQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()

