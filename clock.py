from apscheduler.schedulers.blocking import BlockingScheduler
import os
from os import environ
import re

file = open('key', 'w+')
file.write(environ["KEY"])

DATABASE_NAME = environ["DATABASE_URL"].split("/")[-1]
with open("src/DatabaseCreation.sql", "r+") as myfile:
    data = myfile.read()
    data = re.sub("luc", DATABASE_NAME, data)
    myfile.seek(0)
    myfile.write(data)
    myfile.truncate()

os.system("src/main.py --reset")
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    os.system("src/main.py --update")
    os.system("src/main.py --verify")
