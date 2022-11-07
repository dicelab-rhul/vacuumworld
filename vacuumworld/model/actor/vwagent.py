from typing import Optional

from .vwactor import VWActor
from .vwactormind import VWMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from .vwactuators import VWPhysicalActuator, VWCommunicativeActuator
from ..actions.clean_action import VWCleanAction


class VWCleaningAgent(VWActor):
    '''
    This class specifies the cleaning agent. It is a subclass of `VWActor`.
    '''
    def __init__(self, mind: VWMind) -> None:
        super(VWCleaningAgent, self).__init__(mind=mind, sensors=[VWObservationSensor(), VWListeningSensor()], actuators=[VWPhysicalActuator(), VWCommunicativeActuator()])

    def get_physical_actuator(self) -> Optional[VWPhysicalActuator]:
        '''
        Returns the `VWUserPhysicalActuator` of this `VWCleaningAgent`, or `None`, if it is not available.

        The `VWUserPhysicalActuator` of a `VWCleaningAgent` must support `VWCleanAction`.
        '''
        return super(VWCleaningAgent, self).get_actuator_for(event_type=VWCleanAction)
