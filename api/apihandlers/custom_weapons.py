from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import CustomWeapon

def add_custom_weapon(name:str, damage: int, range: int, db: Session):
    if not name.strip() or not damage.strip():
        raise HTTPException(status_code=400, detail="Name and damage are required/")
    
    # Optionally: check if weapon already exists
    existing = db.query(CustomWeapon).filter(CustomWeapon.name == name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Weapon '{name}' already exists.")
    
    new_weapon = CustomWeapon(name=name, damage=damage, range=range)
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)

    return {f"success: Custom weapon '{new_weapon.name}' added successfully!"}