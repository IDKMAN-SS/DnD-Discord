from fastapi import FastAPI, Depends
from api.apihandlers import roll, lookup, scheduler, custom_weapons, reminders_due
import logging
from database.database import get_db
from sqlalchemy.orm.session import Session

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("running base url")
    return {"message": "Hello World"}

@app.get("/roll")
def _(dice: str = ""):
    logger.debug("rolling endpoint hit")
    if dice == "":
        return{"could not process request"}
    try:
        return roll.roll_dice(dice)
    except ValueError as e:
        return str(e)

@app.get("/reminders_due")
def _(db: Session = Depends(get_db)):
    return reminders_due.get_due_reminder(db)

@app.get("/search")
def _(name: str = "", ltype: str = "", db: Session = Depends(get_db)):
    if name == "" or ltype == "":
        return {"name or type are missing"}
    try:
        return lookup.lookup(name, ltype, db)
    except ValueError as e:
        return str(e)

@app.post("/reminder")
def _(date: str, time: str, message: str, channel_id: str, db: Session = Depends(get_db)):
    if date == "" or time == "":
        return "invalid data please schedule your date as : yyyy-mm-dd and time as : hh:mm"
    if message == "":
        return "please make sure to fill in your message after your date and time"
    if channel_id == "":
        return "Error: could not find channel_id"
    try:
        return scheduler.schedule_reminder(date, time, message, channel_id, db)
    except ValueError as e:
        return str(e)

@app.post("/mark_sent")
def _(reminder_data: dict, db: Session = Depends(get_db)):
    return(reminders_due.mark_sent(reminder_data, db))

@app.post("/customweapon")
def _(name: str, damage: int, range: int, db: Session = Depends(get_db)):
    return custom_weapons.add_custom_weapon(name, damage, range, db)
