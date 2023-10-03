from typing import Iterable, Type

from pystarworldsturbo.elements.actuator import Actuator

from ...actions.vwactions import VWAction
from ...actions.vwmove_action import VWMoveAction
from ...actions.vwturn_action import VWTurnAction
from ...actions.vwclean_action import VWCleanAction
from ...actions.vwdrop_action import VWDropAction
from ...actions.vwidle_action import VWIdleAction
from ...actions.vwspeak_action import VWSpeakAction
from ...actions.vwbroadcast_action import VWBroadcastAction


class VWActuator(Actuator):
    '''
    This class specifies the actuator for `VWActor`. It is a subclass of `Actuator`.
    '''
    def __init__(self, subscribed_events: list[Type[VWAction]]) -> None:
        super(VWActuator, self).__init__(subscribed_events=subscribed_events)

    def source(self) -> Iterable[VWAction]:
        '''
        Fetches all the available `VWAction` instances, and returns either the single `VWAction`, or an `Iterable[VWAction]`.
        '''
        return [a for a in super(VWActuator, self).source_all() if isinstance(a, VWAction)]


class VWPhysicalActuator(VWActuator):
    '''
    This class specifies the physical actuator for `VWCleaningAgent`. It is a subclass of `VWActuator`.
    '''
    def __init__(self) -> None:
        super(VWPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWCleanAction, VWIdleAction])


class VWUserPhysicalActuator(VWActuator):
    '''
    This class specifies the physical actuator for `VWUser`. It is a subclass of `VWActuator`.
    '''
    def __init__(self) -> None:
        super(VWUserPhysicalActuator, self).__init__(subscribed_events=[VWMoveAction, VWTurnAction, VWDropAction, VWIdleAction])


class VWCommunicativeActuator(VWActuator):
    '''
    This class specifies the communicative actuator for `VWActor`. It is a subclass of `VWActuator`.
    '''
    def __init__(self) -> None:
        super(VWCommunicativeActuator, self).__init__(subscribed_events=[VWSpeakAction, VWBroadcastAction])
