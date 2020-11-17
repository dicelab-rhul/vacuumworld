from typing import Iterable, List, Type, Union

from .body import  Body
from .sensor import Sensor
from .actuator import Actuator
from .mind import Mind
from ..common.message import BccMessage
from ..common.action import Action



class Actor(Body):
    def __init__(self, mind: Mind, sensors: List[Sensor]=[], actuators: List[Actuator]=[]) -> None:
        super(Body, self).__init__()

        self.__mind: Mind = mind
        self.__sensors: List[Sensor] = sensors
        self.__actuators: List[Actuator] = actuators

    def get_mind(self) -> Mind:
        return self.__mind

    def get_sensors(self) -> List[Sensor]:
        return self.__sensors

    def get_listening_sensor(self) -> Sensor:
        return self.get_sensor_for(event_type=BccMessage)

    def get_sensor_for(self, event_type: Type) -> Sensor:
        for sensor in self.__sensors:
            if sensor.is_subscribed_to(event_type=event_type):
                return sensor

        return None

    def get_actuators(self) -> List[Actuator]:
        return self.__actuators

    def get_actuator_for(self, event_type: Type) -> Actuator:
        for actuator in self.__actuators:
            if actuator.is_subscribed_to(event_type=event_type):
                return actuator

        return None

    def cycle(_) -> None:
        # Abstract.
        pass

    def get_outstanding_actions(self) -> List[Action]:
        actions: List[Action] = []

        # Any actor must execute at least one action per cycle.
        while not actions:
            actions += self.__get_outstanding_actions()

        return actions

    def __get_outstanding_actions(self) -> List[Action]:
        actions: List[Action] = []

        for actuator in self.__actuators:
            if actuator.has_pending_actions():
                _actions: Union[Action, Iterable[Action]] = actuator.source()

                if type(_actions) == Action:
                    actions.append(_actions)

                else:
                    for a in _actions:
                        actions.append(a)

        return actions
