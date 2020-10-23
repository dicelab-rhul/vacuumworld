from pystarworlds.Agent import Sensor

from ..common.observation import Observation
from ..common.message import Message



class VisionSensor(Sensor):
    subscribe = [Observation]

class CommunicationSensor(Sensor):  # ear for getting a communication perception
    subscribe = [Message]
