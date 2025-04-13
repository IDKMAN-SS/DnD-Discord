from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Character
from database.database import get_db
from roll import roll_dice
import random

router = APIRouter()

#roll for attack value
def roll_attack(character_level, ac):
    attack_roll = random.randint(1, 20) + character_level
    return attack_roll >= ac

@router.post("/attack")
async def attack(attacker_name: str, target_name: str, damage_dice: str, db: Session = Depends(get_db)):
    attacker = db.query(Character).filter(Character.name == attacker_name).first()
    target = db.query(Character).filter(Character.name == target_name).first()
    
    if not attacker or not target:
        raise HTTPException(status_code=404, detail="Attacker or target not found")
    
    #attack
    hit = roll_attack(attacker.level, target.ac)
    
    if not hit:
        return {"message": f"{attacker_name} missed {target_name}!"}
    
    #roll for attack value
    try:
        damage_rolls = roll_dice(damage_dice)
        damage = sum(damage_rolls)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid damage dice format.")
    
    #apply damage if attack hits
    target.hp -= damage
    if target.hp <= 0:
        target.hp = 0
    
    db.commit()
    db.refresh(target)
    
    return {"message": f"{attacker_name} hit {target_name} for {damage} damage. {target_name} now has {target.hp} HP."}
