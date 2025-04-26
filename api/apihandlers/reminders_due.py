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

def mark_sent(reminder_data: dict, db: Session):
    reminder_id = reminder_data.get("id")
    if not reminder_id:
        raise ValueError("Invalid Id")
    db.execute(text("""
        UPDATE reminders SET sent = 1 WHERE id = :id
    """), {"id": reminder_id})
    db.commit()
    return {"message": f"Reminder {reminder_id} marked as sent"}
