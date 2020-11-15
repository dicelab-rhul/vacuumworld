from pystarworldsturbo.common.action import Action
from .body import  Body
from .sensor import Sensor
from .actuator import Actuator
from .mind import Mind
from ..common.message import BccMessage

from typing import List, Type



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

    def get_actuator_for(self, event_type: Type) -> Sensor:
        for actuator in self.__actuators:
            if actuator.is_subscribed_to(event_type=event_type):
                return actuator

        return None

    def get_outstanding_actions(self) -> List[Action]:
        actions: List[Action] = []

        for actuator in self.__actuators:
            if actuator.has_pending_actions():
                actions.append(actuator.source())

        return actions
