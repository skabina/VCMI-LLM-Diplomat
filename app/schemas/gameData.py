from pydantic import BaseModel
from typing import List 

class GameTime(BaseModel):
    month: int
    week: int
    day: int

class Resources(BaseModel):
    gold: int
    wood: int
    ore: int
    mercury: int
    sulfur: int
    crystal: int
    gems: int

class Unit(BaseModel):
    name: str
    count: int

class HeroStats(BaseModel):
    name: str
    hero_class: str
    attack: int
    defense: int
    spell_power: int
    knowledge: int
    current_mana: int
    army: List[Unit]

class MapContext(BaseModel):
    distance_to_player: int 
    terrain: str             
    distance_to_bot_castle: int

class GameContext(BaseModel):
    time: GameTime
    bot_resources: Resources
    player_resources: Resources
    bot_army_value: int = 0
    player_army_value: int = 0
    bot_hero: HeroStats
    player_hero: HeroStats  
    map_info: MapContext
    player_message: str
    bot_personality: str