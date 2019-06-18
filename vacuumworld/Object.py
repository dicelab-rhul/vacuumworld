
from BasicBuildingBlock.Identificaiton import Identifiable
class NonCognitiveObject(Identifiable):
    
    def __init__(self):
      pass 
  
    def getID(self):
     return self.ID# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

class Dirt(NonCognitiveObject):
    def __init__(self, color):
      self.__color__=color
         
    def getColor(self):
        return self.__color__
        