import logging
import re
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def schedule_reminder(date, time, message, channel_id, db: Session):
    pattern = r"([0-9]{4}-[0-1][0-9]-[0-9]{2})\s([0-2][0-9]:[0-9]{2})"
    datetime_str = f"{date} {time}"
    match = re.fullmatch(pattern, datetime_str)
    if not match:
        logger.debug("No match")
        raise ValueError("invalid date and time yyyy-mm-dd and hh:mm")
    date_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    try:
        db.execute(text("""
            INSERT INTO reminders (channel_id, message, date_time)
            VALUES (:channel_id, :message, :date_time)
        """),{
            "channel_id": channel_id,
            "message": message,
            "date_time": date_time
        })
        db.commit()
        logger.debug(f"Reminder added to database")
    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        raise ValueError("Failed to schedule reminder")
    return f"Reminder set for {date_time}"
