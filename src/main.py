# Core game logic such as starting a new game and moving 

import rooms
from player import Player
from enemy import Enemy
from pathlib import Path
import yaml

print("Welcome to the game. ")

projectdir = Path(__file__).resolve().parent.parent
controlFilePath = projectdir / "data" / "controls.yaml"

with open(controlFilePath, 'r') as controlFile:
    controls = yaml.safe_load(controlFile)

roomKey = controls["roomKey"]
attackKey = controls["attackKey"]
healthKey = controls["healthKey"]
moonShadeKey = controls["moonShadeKey"]
vanishPearlKey = controls["vanishPearlKey"]

print("Controls\n---------")
print(f"Move to the next room: {roomKey}")
print(f"Attack: {attackKey}")
print(f"Use Health: {healthKey}")
print(f"Use Moon Shade: {moonShadeKey}")
print(f"Use Vanish Pearl: {vanishPearlKey}")
