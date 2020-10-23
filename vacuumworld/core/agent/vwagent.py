from pystarworlds.Agent import Body

from . import vwsensor
from . import vwactuator
from .mind.vwmind import VWMind

from collections import namedtuple



agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')


class VWBody(Body):
    def __init__(self, _type, id, mind, orientation, coordinate, colour):
        mind = VWMind(mind)
        assert _type in agent_type
        if _type == agent_type.cleaning:
            actuators = [vwactuator.CleaningAgentActuator(), vwactuator.CommunicationActuator()]
        else:
            actuators = [vwactuator.UserActuator(), vwactuator.CommunicationActuator()]

        sensors = [vwsensor.VisionSensor(), vwsensor.CommunicationSensor()]

        self._Identifiable__ID = id # hack...
        mind._Identifiable__ID = id # hack...

        super(VWBody, self).__init__(mind, actuators, sensors)
        
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate
