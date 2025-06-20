# Core game logic such as starting a new game and moving 

import rooms
from player import Player

print("Welcome to the game.")
print("Type anything to level up, or just press Enter to quit.\n")

pl = Player()

while True:
    cmd = input("> ").strip()
    if cmd == "":
        print("Exiting...")
        break
    pl.levelUp()

  

