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

    def megaupgrade(): 
      print(f"You've reached a milestone! \n Increased Luck from {self.luck}% to {self.luck+10}%\n")  
      self.luck+=10

    self.level += 1

    # check for tier upgrade and give mega upgrade.
    if self.level == 6:
        self.playerTier = 2
        self.unlockedLuck = True
        self.luck = 5
        print(f"Attribute Luck has been unlocked! Current Luck: {self.luck}%\n")
    elif self.level == 26:
        self.playerTier = 3
        megaupgrade()
    elif self.level == 51:
        self.playerTier = 4
        megaupgrade()
    elif self.level == 56:
        self.playerTier = 5
        megaupgrade()

    # reset the upgrade limits
    if self.level in (6, 26, 51, 56):    
       self.possibleUpgrades = tierUpgrades[self.playerTier]["limits"].copy()

    self.currentHP = self.maxHP
    self.exp = 0
    self.increaseStats()



  def printStatus(self):  
    print("Current Player Status\n--------\n")
    print(f"Level: {self.level} \n")
    print(f"HP: {self.currentHP} / {self.maxHP} \n")
    print(f"ATK: {self.atk} \n")
    if(self.unlockedLuck):
      print(f"LUCK: {self.luck}%\n")



  def getUpgrade(self, HPamount, ATKamount, LUCKamount):  
    print("Remaining Possible Upgrades, Enter the respective number to upgrade the stat\n")  
    print(f"1. Health: {self.possibleUpgrades['hp']} remaining, {self.currentHP} -> {self.maxHP+HPamount}\n")
    print(f"2. Attack: {self.possibleUpgrades['atk']} remaining, {self.atk} -> {self.atk+ATKamount} \n")
    if(self.unlockedLuck):
      print(f"3. Luck: {self.possibleUpgrades['luck']} remaining, {self.luck}% -> {self.luck+LUCKamount}% \n")

    while True:
      try:
        value = int(input("> "))  
        if (value > 0 and value < 4) and (value == 1 or value == 2 or self.unlockedLuck):
          return value    
        print("Please enter a valid upgrade index.\n")
      except ValueError:
        print("Please enter a number.")




  def increaseStats(self):    

    HPamount = tierUpgrades[self.playerTier]["values"]["hp"]
    ATKamount = tierUpgrades[self.playerTier]["values"]["atk"]
    LUCKamount = tierUpgrades[self.playerTier]["values"]["luck"]

    # first we check if the desired upgrade is available
    while True:
      self.printStatus()
      toUpgrade = self.getUpgrade(HPamount, ATKamount, LUCKamount)
      key = self.statOrder[toUpgrade - 1]
      if (self.possibleUpgrades[key]):
        self.possibleUpgrades[key] -= 1
        break
      print("You cannot upgrade that stat anymore!\n")

    # here we upgrade the desired stat    
    match toUpgrade:
      case 1: # hp case
        print(f"Upgraded HP from {self.maxHP} to {self.maxHP+HPamount}\n")
        self.maxHP += HPamount
      case 2: # atk case  
        print(f"Upgraded ATK from {self.atk} to {self.atk+ATKamount}\n")
        self.atk += ATKamount
      case 3: # luck case  
        print(f"Upgraded LUCK from {self.luck}% to {self.luck+LUCKamount}%\n")
        self.luck += LUCKamount
      case _:  
        raise ValueError(f"in increaseStats() got value {toUpgrade}.")
           
    
