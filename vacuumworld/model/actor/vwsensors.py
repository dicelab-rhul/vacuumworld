from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.common.message import BccMessage

from ...common.observation import Observation



class VWObservationSensor(Sensor):
    def __init__(self) -> None:
        super(VWObservationSensor, self).__init__(subscribed_events=[Observation])

    def source(self) -> Observation:
        return super(VWObservationSensor, self).source()


class VWListeningSensor(Sensor):
    def __init__(self) -> None:
        super(VWListeningSensor, self).__init__(subscribed_events=[BccMessage])

    def source(self) -> BccMessage:
        return super(VWListeningSensor, self).source()
