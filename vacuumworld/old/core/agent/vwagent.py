from typing import Any, List
from vacuumworld.core.common.coordinates import Coord
from vacuumworld.core.common.colour import Colour
from vacuumworld.core.common.orientation import Orientation
from pystarworlds.Agent import Actuator, Body, Sensor

from . import vwsensor
from . import vwactuator
from .mind.vwmind import VWMind

from collections import namedtuple



agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')


class VWBody(Body):
    def __init__(self, _type: str, id: str, mind: Any, orientation: Orientation, coordinate: Coord, colour: Colour):
        mind: VWMind = VWMind(mind)
        assert _type in agent_type
        if _type == agent_type.cleaning:
            actuators: List[Actuator] = [vwactuator.CleaningAgentActuator(), vwactuator.CommunicationActuator()]
        else:
            actuators: List[Actuator] = [vwactuator.UserActuator(), vwactuator.CommunicationActuator()]

        sensors : List[Sensor] = [vwsensor.VisionSensor(), vwsensor.CommunicationSensor()]

        self._Identifiable__ID: str = id # hack...
        mind._Identifiable__ID = id # hack...

        super(VWBody, self).__init__(mind, actuators, sensors)
        
        self.orientation: Orientation = orientation
        self.colour: Colour = colour 
        self.coordinate: Coord = coordinate

    def get_orientation(self) -> Orientation:
        return self.orientation

    def get_colour(self) -> Colour:
        return self.colour

    def get_coordinates(self) -> Coord:
        return self.coordinate

    def get_mind(self) -> VWMind:
        return self.mind

    def get_id(self) -> str:
        return self._Identifiable__ID

    def get_name(self) -> str:
        return self.ID

    def get_sensors(self) -> List[Sensor]:
        return self.sensors

    def get_actuators(self) -> List[Actuator]:
        return self.actuators
