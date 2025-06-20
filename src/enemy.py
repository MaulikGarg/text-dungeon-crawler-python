# This file is responsible for all code related to enemy generation

import yaml

class Enemy:


  def __init__(self):
    self.type = None # common, rare, elite, boss
    self.sight = None # the higher this is, the less odds to sneak escape
    
