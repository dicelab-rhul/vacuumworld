from pystarworlds.Agent import Mind

#from .vwperception import Observation#, Message
from . import vwaction
from . import vwc

from pystarworlds.Agent import AgentBody 

import random


class UserBody(AgentBody):
    
    def __init__(self,name, mind, actuators, sensors, orientation, coordinate, colour):
        super().__init__(name,mind,actuators,sensors)
        self.orientation = orientation
        self.colour = colour
        self.coordiante = coordinate
        

class UserMind(Mind):
       
   def __post_init__(self, body):
        super().__post_init__(body)
        self.percept=None  
  
    #@abstractmethod
   
   def perceive(self):
    super().perceive()
    perceptions=super()._getPerceptions()
  
    
    obser=None
    for per in perceptions:
      if(type(per)==Observation):
         obser=per.observation
     
    #      messages.append(mess)
     
        
    #what is this
    self.percept=vwc.perception(obser,None)
    self.getBody().setCoordinate(self.percept.observation.center.coordinate)
    self.getBody().setOrientation(self.percept.observation.center.agent.direction)
    
   def decide(self):  # deliberate
            
    
       if(self.percept==None):
          print("--zero perception--")
         
       else:
        ### sort perceptions process visionones first and then communication   
        
        if self.percept.observation==None:
            print("No visual perception")
                   
        if(self.percept.observation.center.agent and self.percept.observation.forward==None) or(self.percept.observation.center.agent and self.percept.observation.forward.agent!=None):  # wall or agent in front 
                   
                   print("change orientation")
                   act=vwaction.TurnLeft(self)
              
        elif (self.percept.observation.center.agent and self.percept.observation.center.dirt==None):
                   print("Drop Dirt")
                   r=random.randint(1,3) #what is this?
                   act=vwaction.DropDirt(self) 
                
        elif self.percept.observation.center.agent!=None and self.percept.observation.center.dirt!=None:
                     print("move forward")
                     act=vwaction.Move(self) #what is this?
      
                 
         
        

