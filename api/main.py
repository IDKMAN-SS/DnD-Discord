from fastapi import FastAPI
from api.apihandlers import roll
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

