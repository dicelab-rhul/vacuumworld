from pystarworlds.Sensor import Sensor

from .vwc import observation, message

class VisionSensor(Sensor):

    def __init__(self):
        super(VisionSensor, self).__init__([observation])
     
class CommunicationSensor(Sensor):  # ear for getting a communication perception
   def __init__(self):  
       super().__init__([message])
