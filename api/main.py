from fastapi import FastAPI, Depends
from api.apihandlers import roll, lookup
from sqlalchemy.orm import Session
from api.apihandlers.attack import router as attack_router
import logging
from database.database import get_db
from api_models import CharacterBase  
import api.apihandlers.character_management as character_management
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("running base url")
    return {"message": "Hello World"}

@app.get("/roll")
def _(q: str = ""):
    logger.debug("rolling endpoint hit")
    if q == "":
        return{"could not process request"}
    try:
        return roll.roll_dice(q)
    except ValueError as e:
        return str(e)

@app.get("/search")
def _(name: str = "", ltype: str = "", db: Session = Depends(get_db)):
    if name == "" or ltype == "":
        return {"name or type are missing"}
    try:
        return lookup.lookup(name, ltype, db)
    except ValueError as e:
        return str(e)
#create character endpoint
@app.post("/api/character")
def create_character(character: CharacterBase, db: Session = Depends(get_db)):
    return character_management.create_character(character, db)

#get character endpoint
@app.get("/api/character/{name}")
def get_character(name: str, db: Session = Depends(get_db)):
    return character_management.get_character(name, db)

#update character endpoint
@app.put("/api/character/{name}")
def update_character(name: str, character: CharacterBase, db: Session = Depends(get_db)):
    return character_management.update_character(name, character, db)

#delete character endpoint
@app.delete("/api/character/{name}")
def delete_character(name: str, db: Session = Depends(get_db)):
    return character_management.delete_character(name, db)

#attack endpoint
app.include_router(attack_router, prefix="/api")

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
