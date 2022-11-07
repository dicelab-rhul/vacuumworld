from typing import Optional

from .vwactor import VWActor
from .vwusermind import VWUserMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from .vwactuators import VWUserPhysicalActuator, VWCommunicativeActuator
from ..actions.drop_action import VWDropAction


class VWUser(VWActor):
    '''
    This class specifies the user. It is a subclass of `VWActor`.
    '''
    def __init__(self, mind: VWUserMind) -> None:
        super(VWUser, self).__init__(mind=mind, sensors=[VWObservationSensor(), VWListeningSensor()], actuators=[VWUserPhysicalActuator(), VWCommunicativeActuator()])

    def get_mind(self) -> VWUserMind:
        '''
        Returns the `VWUserMind` of this `VWUser`.
        '''
        return super(VWUser, self).get_mind()

    def get_physical_actuator(self) -> Optional[VWUserPhysicalActuator]:
        '''
        Returns the `VWUserPhysicalActuator` of this `VWUser`, or `None`, if it is not available.

        The `VWUserPhysicalActuator` of a `VWUser` must support `VWDropAction`.
        '''
        return super(VWUser, self).get_actuator_for(event_type=VWDropAction)
