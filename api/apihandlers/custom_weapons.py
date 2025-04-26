from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import CustomWeapon

def add_custom_weapon(name:str, damage: str, range: str, db: Session):
    existing = db.query(CustomWeapon).filter(CustomWeapon.name == name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Weapon '{name}' already exists.")
    damageint = int(damage)
    rangeint = int(range)
    new_weapon = CustomWeapon(name=name, damage=damageint, range=rangeint)
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)

    return {f"success: Custom weapon '{new_weapon.name}' added successfully!"}
