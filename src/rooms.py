# This file is responsible for all code related to room generation.

from pathlib import Path
import random 
import yaml

# get template file path
projectdir = Path(__file__).resolve().parent.parent
templatePath = projectdir / "data" / "room_template.yaml"

# load the template room file
with open(templatePath, "r") as templateFile:
  templates = yaml.safe_load(templateFile)

lightLevels = templates["lightLevels"]
sizeLevels =  templates["sizeLevels"]

def generateRoom(light = None , size = None):
  # if light/size is not given, generate.
  if light is None:
    light = random.randint(0, len(lightLevels) - 1)
  if size is None:  
    size = random.randint(0, len(sizeLevels) - 1)

  if not (0 <= light < len(lightLevels)) or not (0 <= size < len(sizeLevels)):
    raise ValueError(f"Unexpected light/size values in generateRoom(): {light}, {size}")

  return light, size

def printRoom(light, size):

  roomLine = random.choice(templates["roomSpawnLine"])
  lightstr = lightLevels[light]
  sizestr = sizeLevels[size]

  if not (0 <= light < len(lightLevels)) or not (0 <= size < len(sizeLevels)):
    raise ValueError(f"Unexpected light/size values in printRoom(): {light}, {size}")

  # format the line to be printed
  roomLineToPrint = roomLine.format(selectedlighting = lightstr, selectedSize = sizestr)
  print(roomLineToPrint)
