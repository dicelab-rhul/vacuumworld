from pystarworlds.Actuator import Actuator

from . import vwaction

class CleaningAgentActuator(Actuator):
    def __init__(self):
      super(CleaningAgentActuator, self).__init__([vwaction.MoveAction,
                                                   vwaction.TurnAction,
                                                   vwaction.CleanAction]) 
class UserActuator(Actuator):
    def __init__(self):
      super(CleaningAgentActuator, self).__init__([vwaction.MoveAction,
                                                   vwaction.TurnAction,
                                                   vwaction.DropAction]) 
class CommunicationActuator(Actuator):
    def __init__(self):
      super().__init__([vwaction.CommunicativeAction]) 
    
