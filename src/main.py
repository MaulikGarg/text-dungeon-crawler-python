# Core game logic such as starting a new game and moving 

import rooms
from player import Player
from enemy import Enemy
from pathlib import Path
import yaml
import combat

print("Welcome to the game. ")

pl = Player()
for i in range(10):
  pl.levelUp()

en = Enemy()
en.generate(pl)
en.printEnemy()
combat.fight(pl, en)
