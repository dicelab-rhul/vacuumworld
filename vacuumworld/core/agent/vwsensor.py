from typing import List, Type
from pystarworlds.Agent import Sensor

from ..common.observation import Observation
from ..common.message import Message



class VisionSensor(Sensor):
    subscribe: List[Type] = [Observation]

class CommunicationSensor(Sensor):  # ear for getting a communication perception
    subscribe: List[Type] = [Message]
