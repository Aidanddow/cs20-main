# Code from https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds/60244694#60244694

from schedule import Scheduler
import threading
import time
from datetime import timedelta
from django.utils.timezone import now

from django.conf import settings
from .models import Url_PDF, Url_HTML

def remove_record(table, type):

    # Code from @David Robinson at https://stackoverflow.com/questions/10345147/django-query-datetime-for-objects-older-than-5-hours

    time_threshold = now() - timedelta(hours=settings.TUPLE_TTL)

    results = table.objects.filter(created__lt=time_threshold)

    if(results):
        for result in results:
            result.delete()
        
        print("---",len(results),type,"_TUPLE DELETED --- ")

def clean_db():
    print("--- Scheduled Database Cleaning")

    remove_record(Url_PDF, "PDF")
    remove_record(Url_HTML, "HTML")

def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    print("--- Cleaning Scheduler Running (every {n_hours} hours)".format(n_hours = settings.CLEANING_INTERVAL))
    scheduler = Scheduler()
    scheduler.every(settings.CLEANING_INTERVAL).hours.do(clean_db)
    scheduler.run_continuously()