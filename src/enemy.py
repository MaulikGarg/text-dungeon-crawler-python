# This file is responsible for all code related to enemy generation

from email.mime import base
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
    self.level = 0
    self.sight = 0 # the higher this is, the less odds to sneak escape
    self.atk = 0
    self.currentHP = 0
    self.maxHP = 0
    self.res = 0 # resistance to crit hits, opposite for luck in Players
    self.deathEXP = 0 # exp to be dropped on death


  def generateType(self, player: Player):
    
    commonOdds = int(data["enemyOdds"]["common"])
    rareOdds = int(data["enemyOdds"]["rare"])
    eliteOdds = int(data["enemyOdds"]["elite"])
    total = commonOdds+rareOdds+eliteOdds
    if total != 100:
      raise ValueError(f"In generate(), enemy odds total isn't 100%, gotten {total}% instead")

    if(player.level < 5):
      commonOdds = 100
    elif(player.level < 10):  
      commonOdds = 80
      rareOdds = 20

    typerandom = random.randint(1, 100)
    if typerandom <= commonOdds:
      self.type = 'common'
    elif typerandom <= (commonOdds + rareOdds):
      self.type = 'rare'
    else:
        self.type = 'elite'

  def generate(self, player: Player):

    if self.type is None: self.generateType(player)
    

    self.name = random.choice(data["enemyNames"][self.type])

    levelVariance = random.randint(-1, 2)
    self.level = max(1, player.level + levelVariance)

    enemyStatPoints = self.level * data["multipliers"][self.type]
    
    # if the player is lucky, deduct 10% enemyStatePoints
    isLucky = True if random.randint(1,100) <= player.luck else False
    if(isLucky):
      enemyStatPoints -= enemyStatPoints*0.05

    hp_boost, atk_boost, res_boost = self.generateStats(enemyStatPoints)
    self.maxHP = 4 + hp_boost
    self.atk = 2 + atk_boost
    self.res = res_boost

    self.currentHP = self.maxHP

    base = 5 + player.level*0.75
    jitter = random.uniform(-5, 10)
    self.sight = min(90, max(10, int(base + jitter)))
    self.deathEXP = self.calcDeathExp(player.luck)


  def generateStats(self, enemyStatPoints):  

    # first the enemies get a bare minimum to ensure flow
    # This spends 55% of the available points
    hp = max(3, enemyStatPoints * 0.25)
    atk = max(1, enemyStatPoints * 0.30)
    res = max(0, enemyStatPoints * 0.10)

    randomlyAllocatedPoints = enemyStatPoints - (hp+atk+res)

    w1, w2, w3 = random.random(), random.random(), random.random()
    total = w1 + w2 + w3

    hp  += (w1 / total) * randomlyAllocatedPoints * 0.8
    atk += (w2 / total) * randomlyAllocatedPoints * 1.3
    res += ((w3 / total) * randomlyAllocatedPoints) * 1.1

    # max res shouldnt be any more than 40
    res = min(40, res)
    return int(hp), int(atk), int(res)
    

  def printEnemy(self):
    print(f'"{self.name}" - Lv.{self.level} - {self.type}')
    print('-' * 10)
    print(f"HP: {self.currentHP}/{self.maxHP}")
    print(f"ATK: {self.atk}")
    print(f"RES: {self.res}%")
    print(f"SIGHT: {self.sight}%")
    print('-' * 10)


  def calcDeathExp(self, luck: int) -> int:
    baseEXP = max(8,int(self.level * 0.8 * data["typeMultiplier"][self.type]))
    if(luck >= random.randint(1,100)):
      baseEXP *= 1.2
    return int(baseEXP)  
