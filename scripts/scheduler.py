import logging
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

schedule_logger = logging.getLogger('schedule')

scheduler = BackgroundScheduler()

def schedule_main(main, schedule):
    time_parts = schedule.split(":")
    if len(time_parts) != 2:
        schedule_logger.warning("Invalid schedule format. Using default time: 06:00.")
        schedule_logger.warning("Fix the 'SCHEDULE' environment schedule. HH:MM required.")
        schedule = "06:00"
        time_parts = schedule.split(":")

    hour, minute = time_parts
    hour = hour.zfill(2)
    schedule_logger.info(f"Scheduling the job to run at: {hour}:{minute}.")

    scheduler.add_job(
        main,
        CronTrigger(hour=hour, minute=minute),
        id="run_main_job",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()
        schedule_logger.info("Scheduler is running.")
    else:
        schedule_logger.info("Scheduler is already running.")

    last_log_time = datetime.now() - timedelta(minutes=15)
    log_interval = timedelta(minutes=15)

    try:
        while True:
            time.sleep(60)
            current_time = datetime.now()
            if current_time - last_log_time >= log_interval:
                schedule_logger.info(f"Checking schedule...Next run at {hour}:{minute}.")
                last_log_time = current_time
    except (KeyboardInterrupt, SystemExit):
        schedule_logger.info("Shutting down scheduler...")
        if scheduler.running:
            scheduler.shutdown()