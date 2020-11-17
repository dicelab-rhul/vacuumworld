from .vwactor import VWActor
from .vwactormind import VWMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from .vwactuators import VWPhysicalActuator, VWCommunicativeActuator
from ..actions.clean_action import VWCleanAction



class VWCleaningAgent(VWActor):
    def __init__(self, mind: VWMind) -> None:
        super(VWCleaningAgent, self).__init__(mind=mind, sensors=[VWObservationSensor(), VWListeningSensor()], actuators=[VWPhysicalActuator(), VWCommunicativeActuator()])

    def get_physical_actuator(self) -> VWPhysicalActuator:
        return super(VWCleaningAgent, self).get_actuator_for(event_type=VWCleanAction)
