from apscheduler.schedulers.blocking import BlockingScheduler
from Cron import Cron
from datetime import datetime

cron = Cron()

sched = BlockingScheduler(timezone='Asia/Seoul')

sched.add_job(
    cron.run,
    'interval', 
    hours=6, 
    minutes=0, 
    next_run_time=datetime.now()
)

print("started")
sched.start()