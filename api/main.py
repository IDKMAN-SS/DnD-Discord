from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.apihandlers.attack import router as attack_router
from database.database import get_db
from api_models import CharacterBase  
import character_management
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("running base url")
    return {"message": "Hello World"}

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
