from typing import List, Type
from pystarworlds.Agent import Actuator

from ..action.vwaction import MoveAction, TurnAction, CleanAction, DropAction, CommunicativeAction



class CleaningAgentActuator(Actuator):
    subscribe: List[Type] = [MoveAction, TurnAction, CleanAction]

class UserActuator(Actuator):
    subscribe: List[Type] = [MoveAction, TurnAction, DropAction]
    
class CommunicationActuator(Actuator):
    subscribe: List[Type] = [CommunicativeAction]
