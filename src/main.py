# Core game logic such as starting a new game and moving 

import rooms
from player import Player
from enemy import Enemy

print("Welcome to the game. default player level for testing is 30 ")

pl = Player()
pl.level = 30
en = Enemy()

while True:
    resp = int(input("1 to level up, 2 to spawn enemy. "))
    if resp == 1:
        pl.level+=1
    else:    
        en.type = None
        en.generate(pl)
        en.printEnemy()
