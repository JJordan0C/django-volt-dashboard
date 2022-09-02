from django.apps import AppConfig
# from django.db.models.signals import post_migrate, class_prepared
# from .models import BaseEvent

# def create_dealers(sender, **kwargs):
#     from .models import Dealer
    # dealers={
    #     9 : 'Goldbet',
    #     11 : 'Snai',
    #     13 : 'Eurobet',
    #     14 : 'Planetcoin',
    #     15 : 'Stanleybet'
    # }
#     for id, name in dealers.items(): 
#         Dealer.objects.get_or_create(
#             id=id,
#             name=name
#         )
        
# def add_field(sender, **kwargs):
#     print(sender.__name__)
#     # if isinstance(sender, BaseEvent):
#     if sender.__name__ == 'GoldbetEvent':
#         print('diobo')
#         field = sender.get_competition_id
#         field.contribute_to_class(sender, "competition_id")
        
class QuoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quote'
    
    # def ready(self):
        # class_prepared.connect(add_field)
        # post_migrate.connect(create_dealers ,sender=self)