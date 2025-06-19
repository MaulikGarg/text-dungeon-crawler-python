# This file contains the core classes for the player

from pathlib import Path
import yaml

projectdir = Path(__file__).resolve().parent.parent

# load upgrade file for future use
upgradePath = projectdir / "data" / "upgrades.yaml" 
with open(upgradePath, "r") as upgradeFile:
  tierUpgrades = yaml.safe_load(upgradeFile)["tiers"]

class Player:


  def __init__(self):
    self.level = 1
    self.exp = 0
    self.maxHP = 10
    self.currentHP = self.maxHP
    self.atk = 3
    self.luck = 0 # unlocks at player level 5
    self.inventory = {"Health": 1, "Vanish": 1, "Elixir": 1}
    self.possibleUpgrades = {"hp": 3, "atk": 3, "luck": 0} # the remaining possible upgrades in current level space
    self.statOrder = ["hp", "atk", "luck"]
    self.unlockedLuck = False
    self.playerTier = 1



  def levelUp(self):
    self.currentHP = self.maxHP
    self.level += 1
    self.exp = 0
    if self.level > 55:
        self.playerTier = 5
    elif self.level > 50:
        self.playerTier = 4
    elif self.level > 25:
        self.playerTier = 3
    elif self.level > 5:
        self.playerTier = 2
    self.increaseStats()



  def printStatus(self):  
    print("Current Player Status\n--------\n")
    print(f"Level: {self.level} \n")
    print(f"HP: {self.currentHP} / {self.maxHP} \n")
    print(f"ATK: {self.atk} \n")



  def getUpgrade(self):  
    print("Remaining Possible Upgrades, Enter the respective number to upgrade the stat\n")  
    print(f"1. Health: {self.possibleUpgrades['hp']} \n")
    print(f"2. Attack: {self.possibleUpgrades['atk']} \n")
    if(self.unlockedLuck):
      print(f"3. Luck: {self.possibleUpgrades['luck']} \n")

    while True:
      try:
        value = int(input("> "))  
        if (value > 0 and value < 4) and (value == 1 or value == 2 or self.unlockedLuck):
          return value    
        print("Please enter a valid upgrade index.\n")
      except ValueError:
        print("Please enter a number.")


  def increaseStats(self):    

    # first we check if the desired upgrade is available
    while True:
      self.printStatus()
      toUpgrade = self.getUpgrade()
      key = self.statOrder[toUpgrade - 1]
      if (self.possibleUpgrades[key]):
        self.possibleUpgrades[key] -= 1
        break

    # here we upgrade the desired stat    
    match toUpgrade:
      case 1: # hp case
        self.upgradeHP()
      case 2: # atk case  
        self.upgradeATK()
      case 3: # luck case  
        self.upgradeLUCK()
      case _:  
        raise ValueError(f"in increaseStats() got value {toUpgrade}.")
        

  def upgradeHP(self):      
    amount = tierUpgrades[self.playerTier]["hp"]
    print(f"Upgraded HP from {self.maxHP} to {self.maxHP+amount}\n")
    self.maxHP += amount
    
  def upgradeATK(self):      
    amount = tierUpgrades[self.playerTier]["atk"]
    print(f"Upgraded HP from {self.atk} to {self.atk+amount}\n")
    self.atk += amount

  def upgradeLUCK(self):      
    amount = tierUpgrades[self.playerTier]["luck"]
    print(f"Upgraded HP from {self.luck} to {self.luck+amount}\n")
    self.luck += amount
