from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from quote.quote_parser import initial_config
from datetime import datetime

#Turn on timed work
try:
    # Instantiate the scheduler
    scheduler = BackgroundScheduler()
    # The scheduler uses DjangoJobStore()
    
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Set timed tasks, the selection method is interval, and the time interval is 10s
    # Another way is to execute the task at a fixed time from Monday to Friday, the corresponding code is:
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='8', minute='30', second='10',id='task_time')
    
    #scheduler.add_job(initial_config, 'date', run_date=datetime.now(), replace_existing=True,)
    initial_config()
    scheduler.start()
except Exception as e:
    print(e)
    # Stop the timer if there is an error
    scheduler.shutdown()
    