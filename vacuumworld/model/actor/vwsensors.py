from typing import Iterable, Union, List, Type

from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.common.message import BccMessage

from ...common.observation import Observation


class VWSensor(Sensor):
    '''
    This class specifies the sensor for `VWActor`. It is a subclass of `Sensor`.
    '''
    def __init__(self, subscribed_events: List[Type]) -> None:
        super(VWSensor, self).__init__(subscribed_events=subscribed_events)


class VWObservationSensor(VWSensor):
    '''
    This class specifies the `Observation` sensor for `VWActor`. It is a subclass of `VWSensor`.
    '''
    def __init__(self) -> None:
        super(VWObservationSensor, self).__init__(subscribed_events=[Observation])

    def source(self) -> Observation:
        '''
        Fetches and returns an `Observation`.
        '''
        return super(VWObservationSensor, self).source()


class VWListeningSensor(VWSensor):
    '''
    This class specifies the `BccMessage` sensor for `VWActor`. It is a subclass of `VWSensor`.
    '''
    def __init__(self) -> None:
        super(VWListeningSensor, self).__init__(subscribed_events=[BccMessage])

    def source(self) -> Union[BccMessage, Iterable[BccMessage]]:
        '''
        Fetches the single available `BccMessage` or all the available `BccMessage` instances (if more than one is available), and returns either the single `BccMessage`, or an `Iterable[BccMessage]`.
        '''
        messages: List[BccMessage] = []

        while True:
            message: BccMessage = super(VWListeningSensor, self).source()

            if message is None:
                break
            else:
                messages.append(message)

        return messages
