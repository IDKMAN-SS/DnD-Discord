from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Character
from database.database import get_db
from api.apihandlers.roll import roll_dice
from api.api_models import AttackRequest 
import random

router = APIRouter()

# roll for attack value
def roll_attack(ac):
    attack_roll = random.randint(1, 20)
    return attack_roll >= ac

@router.post("/attack")
async def attack(request: AttackRequest, db: Session = Depends(get_db)):
    target = db.query(Character).filter(Character.name == request.target_name).first()
    
    # if not attacker:
    #     raise HTTPException(status_code=404, detail="Attacker not found")
    if not target:
        raise HTTPException(status_code=404, detail="target not found")
    
    # attack
    hit = roll_attack(target.ac)
    
    if not hit:
        return {"message": f"{request.attacker_name} missed {request.target_name}!"}
    
    # roll for attack value
    try:
        damage_rolls = roll_dice(request.damage_dice)
        damage = sum(damage_rolls)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid damage dice format.")
    
    # apply damage if attack hits
    target.hp -= damage
    if target.hp <= 0:
        target.hp = 0
    
    db.commit()
    db.refresh(target)
    
    return {
        "message": f"{request.attacker_name} hit {request.target_name} for {damage} damage! {request.target_name} now has {target.hp} HP.",
        "hp": target.hp,
        "user": target.player_id
    }
