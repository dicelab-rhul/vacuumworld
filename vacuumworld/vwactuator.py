from pystarworlds.Actuator import Actuator

from . import vwaction

class PhysicalActuator(Actuator):
    def __init__(self,l):
      super().__init__(l)
      self.firstattempt=True
    def attempt(self, action):
     if(self.firstattempt):
       super().attempt(action)
       self.firstattempt=False
    
    def act(self):
       self.firstattempt=True
       return super().act() 

class MovementActuator(PhysicalActuator):
    def __init__(self):
      super().__init__([vwaction.ForwardMoveMentAction,
                       vwaction.MoveRightAction,
                       vwaction.MoveLeftAction]) 
    
    
class CommunicationActuator(Actuator):
    def __init__(self):
      super().__init__([ vwaction.SpeakAction, vwaction.BroadcastAction]) 
    
class DropDirtActuator(PhysicalActuator):
    def __init__(self):
      super().__init__([ vwaction.DropDirtAction]) 
 
class CleaningDirtActuator(PhysicalActuator):
    def __init__(self):
      super().__init__([ vwaction.CleanDirtAction]) 
