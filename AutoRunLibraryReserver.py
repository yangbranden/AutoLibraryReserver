import time
import sys
import os
from datetime import datetime, timedelta
import logging
from enum import Enum

from HaydenLibraryReserver import reserve_library

class StudyRoom(Enum):
    # Enum members for room numbers
    ROOM_311A = "311A"
    ROOM_311B = "311B"
    ROOM_311C = "311C"
    ROOM_336 = "336"
    ROOM_342 = "342"
    ROOM_351 = "351"
    ROOM_353 = "353"
    ROOM_355 = "355"
    ROOM_357 = "357"
    ROOM_C13 = "C13"
    ROOM_C15 = "C15"
    ROOM_C17 = "C17"
    ROOM_C19 = "C19"
    ROOM_C38 = "C38"
    ROOM_C40 = "C40"
    ROOM_L52 = "L52"
    ROOM_L54 = "L54"
    ROOM_L56 = "L56"

LOGS_DIR = "C:\\Users\\Branden\\AutoLibraryReserver\\logs"

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

def run_reserve_library(room_number: StudyRoom, hour: int):
    try:
        log_filename = setup_logging()
        redirect_print_to_log(log_filename)

        ROOM_NUMBER = room_number.value
        USERNAME = os.getenv("ASU_USER")
        PASSWORD = os.getenv("ASU_PASS")
        ASU_ID = os.getenv("ASU_ID")

        if USERNAME is None or PASSWORD is None or ASU_ID is None:
            raise Exception("Environment variables not properly set.")

        now = datetime.now()
        next_available_date = now + timedelta(days=7)
        RESERVE_TIME = next_available_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        print(f"({now}) Running reserve_library...")

        reserve_library(ROOM_NUMBER, RESERVE_TIME, USERNAME, PASSWORD, ASU_ID)

        now = datetime.now()
        print(f"{now} Task completed.")
    except Exception as e:
        print(f"Error occurred while running task: {e}")
        return -1
    finally:
        restore_print()
    return 0

def schedule(mon=20,tues=20,wed=20,thurs=20,fri=20,sat=20,sun=20):
    day_of_week = datetime.now().weekday()

    hour = 9
    if day_of_week == 0: # MONDAY
        hour = mon
    elif day_of_week == 1: # TUESDAY
        hour = tues
    elif day_of_week == 2: # WEDNESDAY
        hour = wed
    elif day_of_week == 3: # THURSDAY
        hour = thurs
    elif day_of_week == 4: # FRIDAY
        hour = fri
    elif day_of_week == 5: # SATURDAY
        hour = sat
    elif day_of_week == 6: # SUNDAY
        hour = sun

    return hour

def main():
    ROOM_NUMBER = StudyRoom.ROOM_C19
    HOUR = schedule(mon=20,tues=20,wed=20,thurs=20,fri=20,sat=20,sun=20)

    current_date = datetime.now().date()

    while True:
        now = datetime.now().date()
        if now != current_date:
            try:
                HOUR = schedule(mon=20,tues=20,wed=20,thurs=20,fri=20,sat=20,sun=20)
                if run_reserve_library(ROOM_NUMBER, HOUR) == 0:
                    current_date = now
            except Exception as e:
                # Logs should be recorded in logs file
                continue
        time.sleep(15)

if __name__ == "__main__":
    main()