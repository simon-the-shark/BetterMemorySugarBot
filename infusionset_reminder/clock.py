from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from .settings import SECRET_KEY

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=21)
def scheduled_job():
    requests.get("https://reminder-rekina.herokuapp.com/get/?key={}".format(SECRET_KEY))

sched.start()