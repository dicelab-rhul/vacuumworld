from BasicBuildingBlock.Actuator import Actuator
from GridWorldAction import ForwardMoveMentAction,MoveRightAction,MoveLeftAction,SpeakAction,BroadcastAction, CleanAction,DropAction


class MovementActuator(Actuator):
    def __init__(self):
      super().__init__([ForwardMoveMentAction,MoveRightAction,MoveLeftAction]) 
    
    
class CommunicationActuator(Actuator):
    def __init__(self):
      super().__init__([SpeakAction,BroadcastAction]) 
    
class DropDirtActuator(Actuator):
    def __init__(self):
      super().__init__([DropAction]) 
 
class CleaningDirtActuator(Actuator):
    def __init__(self):
      super().__init__([CleanAction]) 
