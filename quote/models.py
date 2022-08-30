from django.db import models
from .utils import create_model
from django.conf import settings

# Create your models here.


class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=True)

    class SUB_MODEL:
        QUOTE_TYPE = 'QuoteType'
        COMPETITION = 'Competition'
        EVENT = 'Event'
        EVENTQUOTE = 'EventQuote'

    class Meta:
        db_table = "dealers"

    def get_sub_model(self, sub_model):
        return globals()[f'{self.name}{sub_model}']


class GoldbetQuoteType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True, blank=True)
	class Meta:
		db_table = 'goldbet_quote_types'

class GoldbetCompetition(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	pal = models.IntegerField()
	class Meta:
		db_table = 'goldbet_competitions'


class GoldbetEvent(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	competition_id = models.ForeignKey(to=f'quote.GoldbetCompetition', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)
	class Meta:
		db_table = 'goldbet_events'

class GoldbetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(to=f'quote.GoldbetEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.GoldbetQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()
	class Meta:
		db_table = 'goldbet_events_quote'

class SnaiQuoteType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True, blank=True )
	class Meta:
		db_table = 'snai_quote_types'

class SnaiCompetition(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	pal = models.IntegerField()
	class Meta:
		db_table = 'snai_competitions'

class SnaiEvent(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	competition_id = models.ForeignKey(to=f'quote.SnaiCompetition', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)
	class Meta:
		db_table = 'snai_events'

class SnaiEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(to=f'quote.SnaiEvents', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.SnaiQuoteTypes', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()
	class Meta:
		db_table = 'snai_events_quote'

class EurobetQuoteType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True, blank=True )
	class Meta:
		db_table = 'eurobet_quote_types'

class EurobetCompetition(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	pal = models.IntegerField()
	class Meta:
		db_table = 'eurobet_competitions'

class EurobetEvent(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	competition_id = models.ForeignKey(to=f'quote.EurobetCompetition', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)
	class Meta:
		db_table = 'eurobet_events'

class EurobetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(to=f'quote.EurobetEvent', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.EurobetQuoteType', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()
	class Meta:
		db_table = 'eurobet_events_quote'

class PlanetcoinQuoteType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True, blank=True )
	class Meta:
		db_table = 'planetcoin_quote_types'

class PlanetcoinCompetition(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	pal = models.IntegerField()
	class Meta:
		db_table = 'planetcoin_competitions'

class PlanetcoinEvent(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	competition_id = models.ForeignKey(to=f'quote.PlanetcoinCompetition', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)
	class Meta:
		db_table = 'planetcoin_events'

class PlanetcoinEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(to=f'quote.PlanetcoinEvent', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.PlanetcoinQuoteType', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()
	class Meta:
		db_table = 'planetcoin_events_quote'

class StanleybetQuoteType(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True, blank=True )
	class Meta:
		db_table = 'stanleybet_quote_types'

class StanleybetCompetition(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	pal = models.IntegerField()
	class Meta:
		db_table = 'stanleybet_competitions'

class StanleybetEvent(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	competition_id = models.ForeignKey(to=f'quote.StanleybetCompetition', on_delete=models.deletion.CASCADE)
	data = models.DateTimeField(null=True)
	fast_code = models.IntegerField( null=True)
	avv = models.IntegerField( null=True)
	class Meta:
		db_table = 'stanleybet_competitions'

class StanleybetEventQuote(models.Model):
	id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(to=f'quote.StanleybetEvent', on_delete=models.deletion.CASCADE)
	qt_id = models.ForeignKey(to=f'quote.StanleybetQuoteType', on_delete=models.deletion.CASCADE)
	quote = models.FloatField()
	class Meta:
		db_table = 'stanleybet_events_quote'

