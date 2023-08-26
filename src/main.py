from apscheduler.schedulers.blocking import BlockingScheduler
from Cron import Cron
from datetime import datetime

CRON_JOB_ALIVE_DURATION_SECONDS = 60 * 40
CRON_JOB_INTERVAL_HOURS = 4

cron = Cron()

sched = BlockingScheduler(timezone='Asia/Seoul')

sched.add_job(
    cron.run,
    args=[CRON_JOB_ALIVE_DURATION_SECONDS],
    trigget='interval',
    hours=CRON_JOB_INTERVAL_HOURS,
    minutes=0,
    next_run_time=datetime.now()
)

print("started")
sched.start()
