from pystarworlds.Agent import Mind, Body

from . import vwsensor
from . import vwactuator

#maybe this can just be agent body (same as cleaning agent?)
class UserBody(Body):
    
    def __init__(self, ID, mind, orientation, coordinate, colour):
        actuators = {"physical":vwactuator.UserActuator(),
                     "communication":vwactuator.CommunicationActuator()}
        sensors = {"vision":vwsensor.VisionSensor(),
                   "communication":vwsensor.CommunicationSensor()} #can it communicate?
        self.ID = ID
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
                 
         
        

