# api_models.py
from pydantic import BaseModel

class CharacterBase(BaseModel):
    name: str
    player_id: str
    hp: int
    ac: int
    level: int
    race: str
    char_class: str

    class Config:
        from_attributes = True

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: int

    class Config:
        from_attributes = True

class AttackRequest(BaseModel):
    attacker_name: str
    target_name: str
    damage_dice: str
