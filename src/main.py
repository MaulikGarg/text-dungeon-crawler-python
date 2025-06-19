# Core game logic such as starting a new game and moving 

import rooms

print("Welcome to the game. Press any key to generate a new room.\n>")
while(input(">")):
  rooms.printRoom()
