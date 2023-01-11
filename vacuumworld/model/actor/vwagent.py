from typing import cast
from pyoptional.pyoptional import PyOptional

from .vwactor import VWActor
from .mind.vwactor_mind import VWMind
from .appendices.vwsensors import VWListeningSensor, VWObservationSensor
from .appendices.vwactuators import VWPhysicalActuator, VWCommunicativeActuator
from ..actions.vwclean_action import VWCleanAction


class VWCleaningAgent(VWActor):
    '''
    This class specifies the cleaning agent. It is a subclass of `VWActor`.
    '''
    def __init__(self, mind: VWMind) -> None:
        super(VWCleaningAgent, self).__init__(mind=mind, sensors=[VWObservationSensor(), VWListeningSensor()], actuators=[VWPhysicalActuator(), VWCommunicativeActuator()])

    def get_physical_actuator(self) -> PyOptional[VWPhysicalActuator]:
        '''
        Returns the `VWUserPhysicalActuator` of this `VWCleaningAgent`, or `None`, if it is not available.

        The `VWUserPhysicalActuator` of a `VWCleaningAgent` must support `VWCleanAction`.
        '''
        return super(VWCleaningAgent, self).get_actuator_for(event_type=VWCleanAction).filter(lambda actuator: isinstance(actuator, VWPhysicalActuator)).map(lambda actuator: cast(VWPhysicalActuator, actuator))
