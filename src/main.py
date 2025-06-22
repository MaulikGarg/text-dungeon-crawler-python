# Core game logic such as starting a new game and moving 

import player
import rooms
from player import InvItem, Player
from enemy import Enemy
from pathlib import Path
import yaml
from combat import controlMap, fight
import random

mainPlayer = Player() # core player object

print("Welcome to the game. \n")
print("Controls:")
print(f"Attack enemy: {controlMap['attackKey']}")
print(f"Use Health Boost: {controlMap['healthKey']}, to regain health.")
print(f"Use Moon Shade Elixir: {controlMap['moonShadeKey']}, to increase ATK for current combat.")
print(f"Use Vanish Pearl: {controlMap['vanishPearlKey']}, to try and flee combat (can fail).\n")
print("You can only keep 3 each of all the magic items at once.")
print("In darker rooms, enemies have lower sight while high atk")
print("In lighter rooms, enemies have higher sight while low atk")
print("Planning your actions accordingly to the room and Enemy stats is key to winning.\n")
input("Press any keyto start the game.")

bossLevels = [25, 60]

# boss battle executor, checks which boss to fight and summons it
def executeBossFight(player: Player):
  pass

def checkLevelAndReward(player: Player, exp):
  print("You evaded the room successfully.")
  if(mainPlayer.nextLevelEXP <= mainPlayer.exp):
      mainPlayer.levelUp()
  else: 
    print(f"You gained {exp} EXP. Total: {mainPlayer.exp}/{mainPlayer.nextLevelEXP}")
    return
  rewardPool = list(InvItem)
  while True:
    if(len(rewardPool) == 0):
      print("Failed to add a magic item reward as inventory is full.")
      return
    reward = random.choice(rewardPool)
    if(player.inventory[reward]+1 <= 3):
      player.inventory[reward] += 1
      return 
    else:  
      rewardPool.remove(reward)


# game loop for moving room after room
while mainPlayer.level < 61: # at 60, end the game after boss fight
  print('\n' * 30)
  print('-' * 30)
  if mainPlayer.level in bossLevels:
    executeBossFight(mainPlayer)
    continue

  light, size = rooms.generateRoom()
  rooms.printRoom(light, size)

  enemy = Enemy()
  enemy.generate(mainPlayer)
  print(f"You encounter {enemy.name}")

  fightResult = fight(mainPlayer, enemy, light, size)
  exp = 0
  if(fightResult == "victory"):
    exp = enemy.deathEXP
    mainPlayer.exp += exp
    checkLevelAndReward(mainPlayer, exp)
  elif(fightResult == "escape"):  
    exp = int(enemy.deathEXP * 0.5)
    mainPlayer.exp += exp
    checkLevelAndReward(mainPlayer, exp)
  elif(fightResult == "defeat"):  
    print("You died. Game Over.")
    break

  input("Press any key to move to the next room")
