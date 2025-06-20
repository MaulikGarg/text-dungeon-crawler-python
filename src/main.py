# Core game logic such as starting a new game and moving 

import rooms
from player import Player
from enemy import Enemy

print("Welcome to the game.")

pl = Player()
en = Enemy()

while True:
    resp = int(input("1 to level up, 2 to spawn enemy. "))
    if resp == 1:
        pl.levelUp()
    else:    
        en.generate(pl, 'common')
        en.printEnemy()
