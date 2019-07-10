from pystarworlds.Actuator import Actuator
from GridWorldAction import ForwardMoveMentAction,MoveRightAction,MoveLeftAction,SpeakAction, CleanDirtAction,DropDirtAction,BroadcastAction


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
      super().__init__([ForwardMoveMentAction,MoveRightAction,MoveLeftAction]) 
    
    
class CommunicationActuator(Actuator):
    def __init__(self):
      super().__init__([SpeakAction,BroadcastAction]) 
    
class DropDirtActuator(PhysicalActuator):
    def __init__(self):
      super().__init__([DropDirtAction]) 
 
class CleaningDirtActuator(PhysicalActuator):
    def __init__(self):
      super().__init__([CleanDirtAction]) 
