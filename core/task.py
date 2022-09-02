from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apps.quote.quote_parser import initial_config, parse_quote
from datetime import datetime

#Turn on timed work
try:
    # Instantiate the scheduler
    scheduler = BackgroundScheduler()
    # The scheduler uses DjangoJobStore()
    
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    scheduler.add_job(parse_quote, 'interval', minutes=60, replace_existing=True, id='quote_parser')
    initial_config()
    scheduler.start()
except Exception as e:
    print(e)
    # Stop the timer if there is an error
    #scheduler.shutdown()
    