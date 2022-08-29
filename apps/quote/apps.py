from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_dealers(sender, **kwargs):
    from .models import Dealer
    dealers={
        9 : 'Goldbet',
        11 : 'Snai',
        13 : 'Eurobet',
        14 : 'Planetcoin',
        15 : 'Stanleybet'
    }
    for id, name in dealers.items(): 
        Dealer.objects.get_or_create(
            id=id,
            name=name
        )

class QuoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quote'
    
    def ready(self):
        post_migrate.connect(create_dealers ,sender=self)
