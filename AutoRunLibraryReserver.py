import time
import sys
import os
from datetime import datetime, timedelta
import logging

from HaydenLibraryReserver import reserve_library

LOGS_DIR = "logs"

def get_log_filename():
    """Generate a log filename in the format YYYY-MM-DD_logs.txt in the log folder"""
    current_date_str = datetime.now().strftime("%Y-%m-%d")  # e.g., "2024-10-10"
    log_filename = f"{current_date_str}_logs.txt"
    return os.path.join(LOGS_DIR, log_filename)

def setup_logging():
    """Setup logging to a new log file for each day"""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    log_filename = get_log_filename()
    logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")
    return log_filename

def redirect_print_to_log(log_filename):
    """Redirect print statements to the log file"""
    sys.stdout = open(log_filename, 'a')
    sys.stderr = open(log_filename, 'a')

def restore_print():
    """Restore print statements to the console"""
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def run_reserve_library():
    try:
        log_filename = setup_logging()
        redirect_print_to_log(log_filename)
        print("Running reserve_library")

        ROOM_NUMBER = "C19"
        USERNAME = os.getenv("ASU_USER")
        PASSWORD = os.getenv("ASU_PASS")
        ASU_ID = os.getenv("ASU_ID")

        now = datetime.now()
        next_available_date = now + timedelta(days=7)
        RESERVE_TIME = next_available_date.replace(hour=13, minute=0, second=0, microsecond=0)

        reserve_library(ROOM_NUMBER, RESERVE_TIME, USERNAME, PASSWORD, ASU_ID)

        print("Task completed.")
    except Exception as e:
        print(f"Error occurred while running task: {e}")
    finally:
        restore_print()

def main():
    current_date = datetime.now().date()

    while True:
        now = datetime.now()
        if now.date() != current_date:
            try:
                if run_reserve_library() == 0:
                    current_date = now.date()
            except Exception as e:
                # Logs should be recorded in logs file
                continue
        time.sleep(60)

if __name__ == "__main__":
    main()