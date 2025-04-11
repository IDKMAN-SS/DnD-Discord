import logging
import re
from datetime import datetime

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def schedule_reminder(date, time, message):
    pattern = r"([0-9]{4}-[0-1][0-9]-[0-9]{2})\s([0-2][0-9]:[0-9]{2})"
    datetime_str = f"{date} {time}"
    match = re.fullmatch(pattern, datetime_str)
    if not match:
        logger.debug("No match")
        return("invalid date and time yyyy-mm-dd and hh:mm")
    date_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    return f"Reminder set for {date_time}"
