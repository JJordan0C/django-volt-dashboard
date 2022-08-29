from quote.quote_parser import initial_config
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Initialize dealer tables with quote types'

    def handle(self, *args, **options):
        initial_config()
        