from typing import Optional

from .vwactor import VWActor
from .vwusermind import VWUserMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from .vwactuators import VWUserPhysicalActuator, VWCommunicativeActuator
from ..actions.drop_action import VWDropAction


class VWUser(VWActor):
    def __init__(self, mind: VWUserMind) -> None:
        super(VWUser, self).__init__(mind=mind, sensors=[VWObservationSensor(), VWListeningSensor()], actuators=[VWUserPhysicalActuator(), VWCommunicativeActuator()])

    def get_physical_actuator(self) -> Optional[VWUserPhysicalActuator]:
        return super(VWUser, self).get_actuator_for(event_type=VWDropAction)
