import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def get_due_reminder(db: Session):
    now = datetime.now(timezone.utc)
    window = now - timedelta(minutes=5)
    logger.debug(f"Querying betweeen {window} and {now}")
    results = db.execute(text("""
        SELECT * FROM reminders
        WHERE date_time <= :now 
        AND date_time >= :window
        AND sent IS NULL
    """),{
        "now":now,
        "window":window
    }).mappings().all()
    return results
