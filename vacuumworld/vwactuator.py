from pystarworlds.Agent import Actuator

from . import vwaction

class CleaningAgentActuator(Actuator):
    subscribe = [vwaction.MoveAction, vwaction.TurnAction, vwaction.CleanAction]

class UserActuator(Actuator):
    subscribe = [vwaction.MoveAction,vwaction.TurnAction,vwaction.DropAction]
    
class CommunicationActuator(Actuator):
    subscribe = [vwaction.CommunicativeAction]
    
