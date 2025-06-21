# This file is responsible for one combat scene code. It requires player and enemy.

from pathlib import Path
import yaml
from enemy import Enemy
import enemy
from player import Player
import random


projectdir = Path(__file__).resolve().parent.parent
controlFilePath = projectdir / "data" / "controls.yaml"

with open(controlFilePath, 'r') as controlFile:
    controls = yaml.safe_load(controlFile)

roomKey = controls["roomKey"]
attackKey = controls["attackKey"]
healthKey = controls["healthKey"]
moonShadeKey = controls["moonShadeKey"]
vanishPearlKey = controls["vanishPearlKey"]


# covers an entire combat sequence until the enemy's drops are picked.
# or the player evades combat successfully.
def fight(player: Player, enemy: Enemy) -> str:
  
  turn = 0 # 0 represents player, 1 represents enemy
  moonShadeAtk = 0

  while True:
    # first we get the player's choice and let them use their turn.
    choice = getPlayerChoice(player)
    if choice == attackKey:
        playerAttack()
    elif choice == healthKey:
        player.useHealth()
    elif choice == moonShadeKey:    
        moonShadeAtk += useMoonShade()
    elif choice == vanishPearlKey:
        if useVanish(player, enemy): return "escape"
    else:
      raise KeyError(f"Cannot match input key {choice} for any action in fight()")

def getPlayerChoice(player: Player):

  possibleActions = [attackKey]

  print("Available Actions:")
  print(f"Attack ({attackKey})")
  if(player.inventory["Health"]):
    print(f"Use Health Boost ({healthKey})")
    possibleActions.append(healthKey)
  if(player.inventory["Vanish"]): 
    print(f"Use Vanish Pearl ({vanishPearlKey})")
    possibleActions.append(vanishPearlKey)
  if(player.inventory["Elixir"]):  
    print(f"Use Moon Shade Elixir ({moonShadeKey})")
    possibleActions.append(moonShadeKey)

  while True:  
    response = input("> ")
    if response in possibleActions:
      return response
    print("Please enter an available action. ")  

def playerAttack():
  pass

def useMoonShade() -> int:
  return 1

# return True if escape is success
def useVanish(player: Player, enemy: Enemy) -> bool:
  if(player.inventory["Vanish"] < 1):
      raise ValueError(f"cannot call useVanish() when current available are {player.inventory["Vanish"]}")

  player.inventory["Vanish"] -= 1    

  if(enemy.type == 'boss'):
    print(f"You try to escape the {enemy.name}, but it notices you.")
    return False

  escapeChance = player.luck - enemy.sight
  escapeRoll = random.randint(1, 100)

  if escapeRoll <= escapeChance:
        print("You successfully escaped using the Vanish Pearl!")
        return True
  else:
        print("You failed to escape. The enemy blocks your path!")
        return False
