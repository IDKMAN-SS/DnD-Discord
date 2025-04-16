from fastapi import FastAPI, Depends
from api.apihandlers import roll, lookup
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
