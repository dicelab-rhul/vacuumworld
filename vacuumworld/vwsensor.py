from pystarworlds.Agent import Sensor

from .vwc import observation, message

class VisionSensor(Sensor):
    subscribe = [observation]
    pass

class CommunicationSensor(Sensor):  # ear for getting a communication perception
    subscribe = [message]
    pass