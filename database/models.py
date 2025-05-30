from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean, ForeignKey, true
from database.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    player_id = Column(String, index=True)
    hp = Column(Integer)
    ac = Column(Integer)
    level = Column(Integer)
    race = Column(String)
    char_class = Column(String)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String)
    message = Column(String)
    date_time = Column(DateTime)
    sent = Column(Boolean, default=False)

class Weapons(Base):
    __tablename__ = "weapons"

    index = Column(String, primary_key=True, index=True)
    name = Column(String)
    weapon_category = Column(String)
    weapon_range = Column(String)
    category_range = Column(String)
    weight = Column(Float)
    properties = Column(String)
    url = Column(String)
    equipment_category_index = Column(String)
    equipment_category_name = Column(String)
    equipment_category_url = Column(String)
    cost_quantity = Column(Integer)
    cost_unit = Column(String)
    damage_damage_dice = Column(String)
    damage_damage_type_index = Column(String)
    damage_damage_type_name = Column(String)
    damage_damage_type_url = Column(String)
    range_normal = Column(Integer)
    range_long = Column(Float)
    throw_range_normal = Column(Float)
    throw_range_long = Column(Float)
    two_handed_damage_damage_dice = Column(String)
    two_handed_damage_damage_type_index = Column(String)
    two_handed_damage_damage_type_name = Column(String)
    two_handed_damage_damage_type_url = Column(String)
    special = Column(String)

class Monster(Base):
    __tablename__ = "monsters"

    index = Column(String, primary_key=True, index=True)
    name = Column(String)
    size = Column(String)
    type = Column(String)
    alignment = Column(String)
    armor_class = Column(String)
    hit_points = Column(Integer)
    hit_dice = Column(String)
    hit_points_roll = Column(String)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    proficiencies = Column(String)
    damage_vulnerabilities = Column(String)
    damage_resistances = Column(String)
    damage_immunities = Column(String)
    condition_immunities = Column(String)
    languages = Column(String)
    challenge_rating = Column(Float)
    proficiency_bonus = Column(Integer)
    xp = Column(Integer)
    special_abilities = Column(String)
    actions = Column(String)
    legendary_actions = Column(String)
    image = Column(String)
    url = Column(String)
    speed_walk = Column(String)
    speed_swim = Column(String)
    senses_darkvision = Column(String)
    senses_passive_perception = Column(Integer)
    desc = Column(String)
    subtype = Column(String)
    speed_fly = Column(String)
    senses_blindsight = Column(String)
    speed_burrow = Column(String)
    speed_climb = Column(String)
    speed_hover = Column(Integer)
    senses_truesight = Column(String)
    senses_tremorsense = Column(String)
    reactions = Column(String)
    forms = Column(String)

class CustomWeapon(Base):
    __tablename__ = "custom_weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    damage = Column(Integer)
    range = Column(Integer)
