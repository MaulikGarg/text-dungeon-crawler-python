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
    print("Current Player Status\n--------")
    print(f"Level: {self.level}")
    print(f"HP: {self.currentHP} / {self.maxHP}")
    print(f"ATK: {self.atk}")
    if(self.unlockedLuck):
      print(f"LUCK: {self.luck}%")



  def getUpgrade(self, HPamount, ATKamount, LUCKamount):  
    print("\nRemaining Possible Upgrades, Enter the respective number to upgrade the stat\n")  

    possibleChoices = []

    if self.possibleUpgrades["hp"]:
      print(f"1. Health: {self.possibleUpgrades['hp']} remaining, {self.currentHP} -> {self.maxHP+HPamount}")
      possibleChoices.append(1)

    if self.possibleUpgrades["atk"]:  
      print(f"2. Attack: {self.possibleUpgrades['atk']} remaining, {self.atk} -> {self.atk+ATKamount}")
      possibleChoices.append(2)

    if self.unlockedLuck and self.possibleUpgrades["luck"]:
      print(f"3. Luck: {self.possibleUpgrades['luck']} remaining, {self.luck}% -> {self.luck+LUCKamount}%")
      possibleChoices.append(3)

    while True:
      try:
        value = int(input("\n> "))  
        if value in possibleChoices:
          return value    
        print("Please enter a valid upgrade index.\n")
      except ValueError:
        print("Please enter a number.")




  def increaseStats(self):    

    HPamount = tierUpgrades[self.playerTier]["values"]["hp"]
    ATKamount = tierUpgrades[self.playerTier]["values"]["atk"]
    LUCKamount = tierUpgrades[self.playerTier]["values"]["luck"]

    self.printStatus()
    toUpgrade = self.getUpgrade(HPamount, ATKamount, LUCKamount)
    key = self.statOrder[toUpgrade - 1]
    self.possibleUpgrades[key] -= 1

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
           
    
