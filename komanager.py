import os
import shutil
import signal
import sys
import logging
import argparse
from datetime import datetime
from scripts.logger import log_setup
from scripts.scheduler import schedule_main, scheduler
from scripts.settings import create_settings_file, update_settings_file
from scripts.validate_settings import validate_settings
from scripts.yaml_generator import create_library_yaml, create_collection_yaml, create_new_movie_yaml, create_in_history_yaml

logger = logging.getLogger(__name__)
schedule_logger = logging.getLogger('schedule')

os.environ['PYTHONPYCACHEPREFIX'] = os.path.join(os.path.dirname(__file__), 'scripts', '__pycache__')

in_docker = os.getenv("IN_DOCKER", "false").strip().lower() == "true"

config_directory = '/config' if in_docker else os.path.join(os.getcwd(), 'config')
if not os.path.exists(config_directory):
    os.makedirs(config_directory, exist_ok=True)

settings_file_path = os.path.join(config_directory, "overlay-settings.yml")

font_src = '/fonts' if in_docker else os.path.join(os.getcwd(), 'fonts')
font_dest = os.path.join(config_directory, 'fonts')

poster_src = '/posters' if in_docker else os.path.join(os.getcwd(), 'posters')
poster_dest = os.path.join(config_directory, 'posters')

parser = argparse.ArgumentParser(description="Run the main script.")
parser.add_argument('-r', '--run-now', action='store_true', help="Run the script immediately and bypass the schedule.")
parser.add_argument('-t', '--time', type=str, help="Time to schedule the job in HH:MM format", default=os.getenv("SCHEDULE", "06:00"))
    
args = parser.parse_args()
run_now_env = os.getenv("RUN_NOW", "false").strip().lower() == "true"
schedule_time = args.time.strip() if args.time else "06:00"

def graceful_shutdown(signal_num, _):
    schedule_logger.info(f"Received signal {signal_num} ({signal.Signals(signal_num).name}). Initiating graceful shutdown...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    schedule_logger.info("Shutting down script...")
    sys.exit(0)

def copy_new_or_changed_files(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
    
    for root, _, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, relative_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)

if in_docker:
    copy_new_or_changed_files(font_src, font_dest)
    copy_new_or_changed_files(poster_src, poster_dest)

def main():
    log_setup(config_directory)

    if args.run_now or run_now_env:
        logger.info("RUN_NOW is set to true. Running status_overlay.py immediately.")
        main_logic()

        if args.run_now:
            logger.info("Exiting script after manual run.")
            sys.exit(0)
        else:
            logger.info(f"Reverting to scheduled runs.")
            if not scheduler.running:
                schedule_main(main, schedule_time)
    else:
        logger.info("RUN_NOW is set to false. Scheduling status_overlay.py.")
        if not os.path.exists(settings_file_path):
            create_settings_file(config_directory, args.run_now, run_now_env, in_docker)

        now = datetime.now().strftime('%H:%M')
        if now == schedule_time:
            main_logic()
        else:
            logger.info(f"Reverting to scheduled runs.")
            if not scheduler.running:
                schedule_main(main, schedule_time)

def main_logic():
    try:
        if not os.path.exists(settings_file_path):
            create_settings_file(config_directory, args.run_now, run_now_env, in_docker)
            return
        
        update_settings_file(config_directory)

        logger.info("")
        logger.info("Validating settings file...")
        logger.info("")
        if not validate_settings(config_directory):
            logger.error("Validation failed. Please fix the issues in the settings file and rerun the script.")
            return
        
        logger.info("")
        logger.info("Validation successful!")
        logger.info("")
        logger.info("Generating overlay files for Kometa.")
        logger.info("")

        create_library_yaml(config_directory)
        create_collection_yaml(config_directory)
        create_in_history_yaml(config_directory)
        create_new_movie_yaml(config_directory)

        logger.info("All library overlay and collection files created.")
        logger.info("----------------------------------------------------------")
        logger.info("")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    main()
