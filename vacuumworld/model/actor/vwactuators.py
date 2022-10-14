from typing import Iterable, List, Union, Type

from pystarworldsturbo.elements.actuator import Actuator

from ..actions.vwactions import VWAction
from ..actions.move_action import VWMoveAction
from ..actions.turn_action import VWTurnAction
from ..actions.clean_action import VWCleanAction
from ..actions.drop_action import VWDropAction
from ..actions.idle_action import VWIdleAction
from ..actions.speak_action import VWSpeakAction
from ..actions.broadcast_action import VWBroadcastAction



class VWActuator(Actuator):
    def __init__(self, subscribed_events: List[Type]) -> None:
        super(VWActuator, self).__init__(subscribed_events=subscribed_events)

    def source(self) -> Union[VWAction, Iterable[VWAction]]:
        actions: List[VWAction] = []

        while True:
            action: VWAction = super(VWActuator, self).source()

            if not action:
                break
            else:
                actions.append(action)

        return actions


class VWPhysicalActuator(VWActuator):
    def __init__(self) -> None:
        super(VWPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWCleanAction, VWIdleAction])


class VWUserPhysicalActuator(VWActuator):
    def __init__(self) -> None:
        super(VWUserPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWDropAction, VWIdleAction])


class VWCommunicativeActuator(VWActuator):
    def __init__(self) -> None:
        super(VWCommunicativeActuator, self).__init__(subscribed_events=[VWSpeakAction, VWBroadcastAction])
