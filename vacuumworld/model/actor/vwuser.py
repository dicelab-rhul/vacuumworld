from typing import cast
from pyoptional.pyoptional import PyOptional

from .vwactor import VWActor
from .mind.vwactor_mind import VWMind
from .mind.vwuser_mind import VWUserMind
from .appendices.vwsensors import VWListeningSensor, VWObservationSensor
from .appendices.vwactuators import VWUserPhysicalActuator, VWCommunicativeActuator
from ..actions.vwdrop_action import VWDropAction


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
        mind: VWMind = super(VWUser, self).get_mind()

        if isinstance(mind, VWUserMind):
            return mind
        else:
            raise TypeError("The mind of a `VWUser` must be a `VWUserMind`.")

    def get_physical_actuator(self) -> PyOptional[VWUserPhysicalActuator]:
        '''
        Returns the `VWUserPhysicalActuator` of this `VWUser`, or `None`, if it is not available.

        The `VWUserPhysicalActuator` of a `VWUser` must support `VWDropAction`.
        '''
        return super(VWUser, self).get_actuator_for(event_type=VWDropAction).filter(lambda actuator: isinstance(actuator, VWUserPhysicalActuator)).map(lambda actuator: cast(VWUserPhysicalActuator, actuator))
