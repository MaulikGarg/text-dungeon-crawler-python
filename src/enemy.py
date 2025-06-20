# This file is responsible for all code related to enemy generation

import yaml
from pathlib import Path
from player import Player
import random

projectdir = Path(__file__).resolve().parent.parent
enemyDataPath = projectdir / "data" / "enemyData.yaml"

with open(enemyDataPath, 'r') as enemyFile:
  data = yaml.safe_load(enemyFile)

class Enemy:

  def __init__(self):
    self.type = None # common, rare, elite, boss
    self.level = None
    self.sight = None # the higher this is, the less odds to sneak escape
    self.atk = None 
    self.hp = None
    self.res = None # resistance to crit hits, opposite for luck in Players

  def generate(self, player: Player):


    enemyStatePoints = player.level * data["multipliers"][self.type]
    
    # if the player is lucky, deduct 10% enemyStatePoints
    isLucky = True if random.randint(1,100) <= player.luck else False
    if(isLucky):
      enemyStatePoints -= enemyStatePoints*0.1
    self.level = int(enemyStatePoints)  

    # now we spend the enemy points 
