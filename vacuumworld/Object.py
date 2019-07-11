
from pystarworlds.Identifiable import Identifiable
class NonCognitiveObject(Identifiable):
    
    def __init__(self):
      pass 
  
    def getID(self):
     return self.ID# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

class Dirt(NonCognitiveObject):
    def __init__(self, colour):
      self.__colour__=colour
         
    def getColour(self):
        return self.__colour__
        