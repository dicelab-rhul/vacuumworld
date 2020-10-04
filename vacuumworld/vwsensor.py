from pystarworlds.Agent import Sensor

from .vwc import Observation, Message

class VisionSensor(Sensor):
    subscribe = [Observation]

class CommunicationSensor(Sensor):  # ear for getting a communication perception
    subscribe = [Message]
