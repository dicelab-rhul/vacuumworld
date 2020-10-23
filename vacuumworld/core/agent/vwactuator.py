from pystarworlds.Agent import Actuator

from ..action.vwaction import MoveAction, TurnAction, CleanAction, DropAction, CommunicativeAction



class CleaningAgentActuator(Actuator):
    subscribe = [MoveAction, TurnAction, CleanAction]

class UserActuator(Actuator):
    subscribe = [MoveAction, TurnAction, DropAction]
    
class CommunicationActuator(Actuator):
    subscribe = [CommunicativeAction]
