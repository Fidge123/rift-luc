from apscheduler.schedulers.blocking import BlockingScheduler
import os

os.system("src/main.py --reset")
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    os.system("src/main.py --update")
    os.system("src/main.py --verify")
