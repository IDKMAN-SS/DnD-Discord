from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Character
import logging

logger = logging.getLogger("uvicorn.error")

#create character
def create_character(character: Character, db: Session):
    logger.debug(f"Creating character: {character.name}")
    existing = db.query(Character).filter(Character.name == character.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Character already exists")
      
    to_add = Character(**character.model_dump())
    db.add(to_add)
    db.commit()
    return {"message": "Character created", "character": to_add}

#get character
def get_character(name: str, db: Session):
    logger.debug(f"Fetching character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

#update character
def update_character(name: str, character_data: Character, db: Session):
    logger.debug(f"Updating character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    for key, value in character_data.model_dump().items():
        setattr(char, key, value)

    db.commit()
    return {"message": "Character updated", "character": char}

#delete character
def delete_character(name: str, db: Session):
    logger.debug(f"Deleting character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    db.delete(char)
    db.commit()
    return {"message": f"Character '{name}' deleted"}
