from typing import Iterable, List, Type, cast
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.common.message import BccMessage

from ....common.vwobservation import VWObservation


class VWSensor(Sensor):
    '''
    This class specifies the sensor for `VWActor`. It is a subclass of `Sensor`.
    '''
    def __init__(self, subscribed_events: List[Type]) -> None:
        super(VWSensor, self).__init__(subscribed_events=subscribed_events)


class VWObservationSensor(VWSensor):
    '''
    This class specifies the `VWObservation` sensor for `VWActor`. It is a subclass of `VWSensor`.
    '''
    def __init__(self) -> None:
        super(VWObservationSensor, self).__init__(subscribed_events=[VWObservation])

    def source(self) -> PyOptional[VWObservation]:
        '''
        Fetches and returns a `VWObservation`.
        '''
        return super(VWObservationSensor, self).source().filter(lambda observation: isinstance(observation, VWObservation)).map(lambda observation: cast(VWObservation, observation))


class VWListeningSensor(VWSensor):
    '''
    This class specifies the `BccMessage` sensor for `VWActor`. It is a subclass of `VWSensor`.
    '''
    def __init__(self) -> None:
        super(VWListeningSensor, self).__init__(subscribed_events=[BccMessage])

    def source(self) -> Iterable[BccMessage]:
        '''
        Fetches all the available `BccMessage` instances, and returns either the single `BccMessage`, or an `Iterable[BccMessage]`.
        '''
        return [m for m in super(VWListeningSensor, self).source_all() if isinstance(m, BccMessage)]
