import os
import logging
from logging.handlers import RotatingFileHandler

def log_setup(config_directory):
    log_directory = os.path.join(config_directory, "logs")
    log_path = os.path.join(log_directory, "manager.log")
    need_roll = os.path.isfile(log_path)

    directory_existed = os.path.exists(log_directory)
    os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()
        
    log_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)-9s %(message)s', "%m/%d/%Y %H:%M")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    if not directory_existed:
        logger.info(f"No log directory at '{log_directory}'. Log folder created.")

    if need_roll:
        log_handler.doRollover()

        original_creation_time = os.path.getctime(log_path + ".1")
        set_creation_time(log_path, original_creation_time)

    logger.info("----------------------------------------------------------")
    logger.info(f"Logging started. Logs located at '{log_path}'.")

    apscheduler_logger = logging.getLogger('apscheduler')
    apscheduler_logger.setLevel(logging.WARNING)
    if apscheduler_logger.hasHandlers():
        apscheduler_logger.handlers.clear()
    apscheduler_console_handler = logging.StreamHandler()
    apscheduler_console_handler.setFormatter(log_formatter)
    apscheduler_logger.addHandler(apscheduler_console_handler)
    apscheduler_logger.propagate = False

    schedule_logger = logging.getLogger('schedule')
    schedule_logger.setLevel(logging.INFO)
    if schedule_logger.hasHandlers():
        schedule_logger.handlers.clear()
    schedule_console_handler = logging.StreamHandler()
    schedule_console_handler.setFormatter(log_formatter)
    schedule_logger.addHandler(schedule_console_handler)
    schedule_logger.propagate = False

def set_creation_time(filename, creation_time):
    if os.name == 'posix':
        # For UNIX-like systems
        os.utime(filename, (creation_time, creation_time))
    elif os.name == 'nt':
        # For Windows systems
        import pywintypes
        import win32file
        import win32con

        creation_time = pywintypes.Time(creation_time)
        winfile = win32file.CreateFile(
            filename, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_READ | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING, 0, None
        )
        win32file.SetFileTime(winfile, creation_time, None, None)
        winfile.close()