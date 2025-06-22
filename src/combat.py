# This file is responsible for one combat scene code. It requires player and enemy.

from pathlib import Path
import yaml
from enemy import Enemy
import enemy
from player import Player
from player import InvItem
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
  
  moonShadeAtk = 0

  while True:
    # first we get the player's choice and let them use their turn.
    choice = getPlayerChoice(player)
    if choice == attackKey:
        playerAttack(player, enemy, moonShadeAtk)
        if not enemy.currentHP: return "victory"
    elif choice == healthKey:
        player.useHealth()
    elif choice == moonShadeKey:    
        moonShadeAtk += useMoonShade(player)
        print(f"Moon Shade Elixir used! Boosted ATK this turn: {moonShadeAtk}")
    elif choice == vanishPearlKey:
        if useVanish(player, enemy): return "escape"
    else:
      raise KeyError(f"Cannot match input key {choice} for any action in fight()")

    
    # now it is the enemy's turn
    enemyAttack(player, enemy)
    if not player.currentHP:
      return "defeat"



def getPlayerChoice(player: Player):

  possibleActions = [attackKey]

  print("Available Actions:")
  print(f"Attack ({attackKey})")

  if(player.inventory[InvItem.HEALTH]):
    print(f"Use Health Boost ({healthKey})")
    possibleActions.append(healthKey)

  if(player.inventory[InvItem.MOON_SHADE_ELIXIR]):  
    print(f"Use Moon Shade Elixir ({moonShadeKey})")
    possibleActions.append(moonShadeKey)

  if(player.inventory[InvItem.VANISH_PEARL]): 
    print(f"Use Vanish Pearl ({vanishPearlKey})")
    possibleActions.append(vanishPearlKey)


  while True:  
    response = input("> ")
    if response in possibleActions:
      return response
    print("Please enter an available action. ")  






def playerAttack(player: Player, enemy: Enemy, moonShadeAtk):
  DMG = player.atk + moonShadeAtk

  critChance = player.luck - enemy.res
  hasCrit = False
  if(random.randint(1, 100) <= critChance):
    print("Your attack crits!")
    DMG *= 1.3
    DMG = int(DMG)

  enemy.currentHP -= DMG
  enemy.currentHP = max(0, enemy.currentHP)

  print(f"You deal {DMG} damage.")  
  if(enemy.currentHP): print(f"It has {enemy.currentHP}/{enemy.maxHP} HP left.\n")
  

def enemyAttack(player: Player, enemy: Enemy):
  # the enemy will get a dmg bonus based on how low their current HP is
  hpRatio = enemy.currentHP/enemy.maxHP if (enemy.maxHP > 0) else 1
  bonusMultiplier = 1.0 + (1.0 - hpRatio) * 0.5 
  
  DMG = int(enemy.atk * bonusMultiplier)
  player.currentHP -= DMG
  player.currentHP = max(0, player.currentHP)

  print(f"{enemy.name} attacks! Deals {DMG} damage.")
  if(player.currentHP): print(f"You have {player.currentHP}/{player.maxHP} HP left.\n")



def useMoonShade(player: Player) -> int:
  if(player.inventory[InvItem.MOON_SHADE_ELIXIR] < 1):
      raise ValueError(f"cannot call useMoonShade() when current available are {player.inventory[InvItem.MOON_SHADE_ELIXIR]}")

  player.inventory[InvItem.MOON_SHADE_ELIXIR] -= 1    
  print(f"Remaining Moon Shade Elixir: {player.inventory[InvItem.MOON_SHADE_ELIXIR]}")

  boostedAtk = max(3,player.atk * 0.25)
  if(random.randint(1,100) < player.luck):
    boostedAtk *= 1.3 

  return int(boostedAtk)



# return True if escape is success
def useVanish(player: Player, enemy: Enemy) -> bool:
  if(player.inventory[InvItem.VANISH_PEARL] < 1):
      raise ValueError(f"cannot call useVanish() when current available are {player.inventory[InvItem.VANISH_PEARL]}")

  player.inventory[InvItem.VANISH_PEARL] -= 1    
  print(f"Remaining Vanish Pearl: {player.inventory[InvItem.VANISH_PEARL]}")
  if(enemy.type == 'boss'):
    print(f"You try to escape the {enemy.name}, but its aura shield makes it impossible.")
    return False

  escapeChance = player.luck - enemy.sight
  escapeRoll = random.randint(1, 100)

  if escapeRoll <= escapeChance:
        print("You successfully escaped using the Vanish Pearl!")
        return True
  else:
        print("You failed to escape. The enemy blocks your path!")
        return False
