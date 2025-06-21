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
    self.type = None # common, rare, elite, boss, 1 through 4
    self.level = None
    self.sight = 0 # the higher this is, the less odds to sneak escape
    self.atk = 0
    self.currHP = 0
    self.hp = 0
    self.res = None # resistance to crit hits, opposite for luck in Players


  def generateType(self):
    commonOdds = int(data["enemyOdds"]["common"])
    rareOdds = int(data["enemyOdds"]["rare"])
    eliteOdds = int(data["enemyOdds"]["elite"])
    total = commonOdds+rareOdds+eliteOdds
    if total != 100:
      raise ValueError(f"In generate(), enemy odds total isn't 100%, gotten {total}% instead")

    typerandom = random.randint(1, 100)
    if typerandom <= commonOdds:
      self.type = 'common'
    elif typerandom <= (commonOdds + rareOdds):
      self.type = 'rare'
    else:
        self.type = 'elite'

  def generate(self, player: Player):

    if self.type is None: self.generateType()

    self.name = random.choice(data["enemyNames"][self.type])

    enemyStatPoints = (player.level+3) * data["multipliers"][self.type]
    
    # if the player is lucky, deduct 10% enemyStatePoints
    isLucky = True if random.randint(1,100) <= player.luck else False
    if(isLucky):
      enemyStatPoints -= enemyStatPoints*0.1

    self.level = int(enemyStatPoints)  
    hp_boost, atk_boost, res_boost = self.generateStats(enemyStatPoints)
    self.hp = 2 + hp_boost
    self.atk = 1 + atk_boost
    self.res = 1 + res_boost

    self.currHP = self.hp

    base = 2 + player.level*0.5
    jitter = random.uniform(-3, 5)
    self.sight = min(100, max(5, int(base + jitter)))

  def generateStats(self, enemyStatPoints):  

    # first the enemies get a bare minimum to ensure flow
    # This spends 55% of the available points
    hp = max(3, enemyStatPoints * 0.30)
    atk = max(1, enemyStatPoints * 0.20)
    res = max(0, enemyStatPoints * 0.05)

    randomlyAllocatedPoints = enemyStatPoints - (hp+atk+res)

    w1, w2, w3 = random.random(), random.random(), random.random()
    total = w1 + w2 + w3

    hp  += (w1 / total) * randomlyAllocatedPoints * 1.1
    atk += (w2 / total) * randomlyAllocatedPoints * 1.0
    res += ((w3 / total) * randomlyAllocatedPoints) * 1.5

    # max res shouldnt be any more than 40
    res = min(40, res)
    return int(hp), int(atk), int(res)
    

  def printEnemy(self):
    print(f'"{self.name}" - Lv.{self.level} - {self.type}')
    print("---------")
    print(f"HP: {self.currHP}/{self.hp}")
    print(f"ATK: {self.atk}")
    print(f"RES: {self.res}%")
    print(f"SIGHT: {self.sight}%")
