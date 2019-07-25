from pystarworlds.Agent import Mind

from pystarworlds.Agent import AgentBody 

#maybe this can just be agent body (same as cleaning agent?)
class UserBody(AgentBody):
    
    def __init__(self, mind, actuators, sensors, orientation, coordinate, colour):
        super(UserBody, self).__init__(mind, actuators, sensors)
        self.orientation = orientation
        self.colour = colour
        self.coordiante = coordinate
        

class UserMind(Mind):
       
   def __post_init__(self, body):
        super(UserMind, self).__post_init__(body)
  
   def perceive(self):
       pass
    
   def decide(self): 
       pass
                 
         
        

