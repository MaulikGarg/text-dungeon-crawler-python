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
    self.name = "enemy" # name to be picked
    self.type = None # common, rare, elite, boss
    self.level = None
    self.sight = None # the higher this is, the less odds to sneak escape
    self.atk = None 
    self.currHP = None
    self.hp = None
    self.res = None # resistance to crit hits, opposite for luck in Players



  def generate(self, player: Player, type):
    self.type = type
    enemyStatPoints = (player.level+3) * data["multipliers"][self.type]
    
    # if the player is lucky, deduct 10% enemyStatePoints
    isLucky = True if random.randint(1,100) <= player.luck else False
    if(isLucky):
      enemyStatPoints -= enemyStatPoints*0.1

    self.level = int(enemyStatPoints)  
 
    self.hp, self.atk, self.res = self.generateStats(enemyStatPoints)

    self.currHP = self.hp


  def generateStats(self, enemyStatPoints):  

    # first the enemies get a bare minimum to ensure flow
    # This spends 28% of the available points
    hp = max(3, enemyStatPoints * 0.15)
    atk = max(1, enemyStatPoints * 0.08)
    res = max(0, enemyStatPoints * 0.05)

    randomlyAllocatedPoints = enemyStatPoints - (hp+atk+res)

    w1, w2, w3 = random.random(), random.random(), random.random()
    total = w1 + w2 + w3

    hp  += (w1 / total) * randomlyAllocatedPoints
    atk += (w2 / total) * randomlyAllocatedPoints
    res += ((w3 / total) * randomlyAllocatedPoints) * 1.5

    return int(hp), int(atk), int(res)
    

  def printEnemy(self):
    print(f"{self.name} - {self.level} - {self.type}")
    print("---------")
    print(f"HP: {self.currHP}/{self.hp}")
    print(f"ATK: {self.atk}")
    print(f"RES: {self.res}%")
    print(f"SIGHT: {self.sight}%")
