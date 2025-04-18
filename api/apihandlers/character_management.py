from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Character
from api.api_models import CharacterCreate, CharacterUpdate, CharacterOut
import logging

logger = logging.getLogger("uvicorn.error")

#create character
def create_character(character: CharacterCreate, db: Session):
    logger.debug(f"Creating character: {character.name}")
    existing = db.query(Character).filter(Character.name == character.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Character already exists")

    to_add = Character(**character.model_dump())
    db.add(to_add)
    db.commit()
    db.refresh(to_add)
    return {"message": "Character created", "character": CharacterOut.from_orm(to_add)}

#get character
def get_character(name: str, db: Session):
    logger.debug(f"Fetching character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterOut.from_orm(char)

#update character
def update_character(name: str, character_data: CharacterUpdate, db: Session):
    logger.debug(f"Updating character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    for key, value in character_data.model_dump(exclude_unset=True).items():
        setattr(char, key, value)

    db.commit()
    db.refresh(char)
    return {"message": "Character updated", "character": CharacterOut.from_orm(char)}

#delete character
def delete_character(name: str, db: Session):
    logger.debug(f"Deleting character: {name}")
    char = db.query(Character).filter(Character.name == name).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    db.delete(char)
    db.commit()
    return {"message": f"Character '{name}' deleted"}
