import logging
from sqlalchemy.orm import Session
from database.models import Monster, Weapons, CustomWeapon

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

def lookup(name, ltype: str, db: Session):
    result = ""
    if(ltype.lower() == "monster"):
        logger.debug("monster path")
        monster = db.query(Monster).filter(Monster.name == name).first()
        if monster != None:
            result = {"Monster Name" : monster.name, "Monster Type" : monster.type, "Monster actions" : monster.actions, "Monster armor" : monster.armor_class, "Monster immunites" : monster.damage_immunities, "Monster Vulnerabilities" : monster.damage_vulnerabilities}
        else:
            raise ValueError(f"{name} is not contained in our database at this time sorry for the inconvience")
    elif(ltype.lower() == "weapon"):
        logger.debug("weapon path")
        weapons: Weapons = db.query(Weapons).filter(Weapons.name == name).first()
        if weapons != None:
            result = {"Weapon Name" : weapons.name, "Weapon Damage" : weapons.damage_damage_dice, "Weapon Prop" : weapons.properties,"Weapon cat" : weapons.weapon_category}
        else:
            raise ValueError(f"{name} is not contained in our database at this time sorry for the inconvience")
    elif(ltype.lower() == "custom weapon"):
        logger.debug("custom path")
        cus_weapon: CustomWeapon = db.query(CustomWeapon).filter(CustomWeapon.name == name).first()
        if cus_weapon != None:
            result = {"Weapon Name": cus_weapon.name, "Weapon Damage": cus_weapon.damage, "Weapon Range": cus_weapon.range}
        else:
            raise ValueError(f"{name} is not contained in the custom weapons db")
    else:
        logger.debug("Invalid type")
        raise ValueError("type is invalid try monster or weapon")
    return result
