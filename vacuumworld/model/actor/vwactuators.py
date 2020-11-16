from pystarworldsturbo.elements.actuator import Actuator

from ..actions.move_action import VWMoveAction
from ..actions.turn_action import VWTurnAction
from ..actions.clean_action import VWCleanAction
from ..actions.drop_action import VWDropAction
from ..actions.idle_action import VWIdleAction
from ..actions.speak_action import VWSpeakAction
from ..actions.broadcast_action import VWBroadcastAction



class VWPhysicalActuator(Actuator):
    def __init__(self) -> None:
        super(VWPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWCleanAction, VWIdleAction])


class VWUserPhysicalActuator(Actuator):
    def __init__(self) -> None:
        super(VWUserPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWDropAction, VWIdleAction])


class VWCommunicativeActuator(Actuator):
    def __init__(self) -> None:
        super(VWCommunicativeActuator, self).__init__(subscribed_events=[VWSpeakAction, VWBroadcastAction])
