from pystarworlds.Actuator import Actuator
from GridWorldAction import ForwardMoveMentAction,MoveRightAction,MoveLeftAction,SpeakAction, CleanDirtAction,DropDirtAction,BroadcastAction


class MovementActuator(Actuator):
    def __init__(self):
      super().__init__([ForwardMoveMentAction,MoveRightAction,MoveLeftAction]) 
    
    
class CommunicationActuator(Actuator):
    def __init__(self):
      super().__init__([SpeakAction,BroadcastAction]) 
    
class DropDirtActuator(Actuator):
    def __init__(self):
      super().__init__([DropDirtAction]) 
 
class CleaningDirtActuator(Actuator):
    def __init__(self):
      super().__init__([CleanDirtAction]) 
