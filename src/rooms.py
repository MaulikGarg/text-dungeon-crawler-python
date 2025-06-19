# This file is responsible for all code related to room generation.

from pathlib import Path
import random 
import yaml

# get template file path
srcDir = Path(__file__).resolve().parent
templatePath = srcDir.parent / "data" / "room_template.yaml"

# load the template room file
with open(templatePath, "r") as templateFile:
  templates = yaml.safe_load(templateFile)

def generateRoom():
  light = random.choice(templates["lightLevels"])
  size =  random.choice(templates["sizeLevels"])
  return light, size

def printRoom(light = None , size = None):
  roomLine = random.choice(templates["roomSpawnLine"])

  # if the lighting or size is not provided for the room,
  # generate it randomly.
  if not (light) or not (size):
    light, size = generateRoom()
  
  # format the line to be printed
  roomLineToPrint = roomLine.format(selectedlighting = light, selectedSize = size)
  print(roomLineToPrint)
