from typing import List, Tuple, Iterable

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.elements.actuator import Actuator
from pystarworldsturbo.elements.actor import Actor

from .vwactormind import VWMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from ..actions.vwactions import VWAction, VWPhysicalAction, VWCommunicativeAction
from ..actions.speak_action import VWSpeakAction
from ...common.observation import Observation
from ...utils.exceptions import VWActionAttemptException



class VWActor(Actor):
    def __init__(self, mind: VWMind, sensors: List[Sensor], actuators: List[Actuator]) -> None:
        super(VWActor, self).__init__(mind=mind, sensors=sensors, actuators=actuators)

    def get_mind(self) -> VWMind:
        return super(VWActor, self).get_mind()

    def get_listening_sensor(self) -> VWListeningSensor:
        return super(VWActor, self).get_listening_sensor()

    def get_observation_sensor(self) -> VWObservationSensor:
        return super(VWActor, self).get_sensor_for(event_type=Observation)

    def get_physical_actuator(_) -> Actuator:
        # Abstract.
        pass

    def get_communicative_actuator(self) -> Actuator:
        return super(VWActor, self).get_actuator_for(event_type=VWSpeakAction) # Works for VWBroadcastAction as well.

    def perceive(self) -> Tuple[Observation, Iterable[BccMessage]]:
        observation: Observation = None
        messages: List[BccMessage] = []

        if self.get_listening_sensor().has_perception():
            messages += self.get_listening_sensor().source()

        if self.get_observation_sensor().has_perception():
            observation = self.get_observation_sensor().source()

        return observation, messages

    def cycle(self) -> None:
        observation, messages = self.perceive()

        self.get_mind().revise(observation=observation, messages=messages)

        self.get_mind().decide()

        actions_to_attempt: Tuple[VWAction] = self.get_mind().execute()

        self.__attempt_actions(actions=actions_to_attempt)

    def __attempt_actions(self, actions: Tuple[VWAction]) -> None:
        for action in actions:
            action.set_actor_id(self.get_id())
            
            actuator: Actuator = None

            if isinstance(action, VWPhysicalAction):
                actuator = self.get_physical_actuator()
            elif isinstance(action, VWCommunicativeAction):
                actuator = self.get_communicative_actuator()

            if not actuator:
                raise VWActionAttemptException("No actuator found for {}.".format(type(action)))
            else:
                actuator.sink(action=action)
