from typing import List, Tuple, Iterable, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.elements.actuator import Actuator
from pystarworldsturbo.elements.actor import Actor

from .actor_behaviour_debugger import ActorBehaviourDebugger
from .vwactormind import VWMind
from .vwsensors import VWListeningSensor, VWObservationSensor
from ..actions.vwactions import VWAction, VWPhysicalAction, VWCommunicativeAction
from ..actions.speak_action import VWSpeakAction
from ..actions.broadcast_action import VWBroadcastAction
from ...common.observation import Observation
from ...common.exceptions import VWActionAttemptException


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
        candidate: Actuator = super(VWActor, self).get_actuator_for(event_type=VWSpeakAction)

        assert candidate.is_subscribed_to(event_type=VWBroadcastAction)

        return candidate

    def perceive(self) -> Tuple[Observation, Iterable[BccMessage]]:
        observations: List[Observation] = self.__fetch_observations()
        messages: List[BccMessage] = self.__fetch_messages()

        assert len(observations) > 0

        if len(observations) > 1:
            return self.__merge_observations(observations), messages
        else:
            return observations[0], messages

    def __fetch_observations(self) -> List[Observation]:
        observations: List[Observation] = []

        # There can be more than one `Observation` if more than one `VWAction` has been attempted.
        while self.get_observation_sensor().has_perception():
            observations.append(self.get_observation_sensor().source())

        return observations

    def __fetch_messages(self) -> List[BccMessage]:
        messages: List[BccMessage] = []

        if self.get_listening_sensor().has_perception():
            tmp: Union[BccMessage, Iterable[BccMessage]] = self.get_listening_sensor().source()

            if isinstance(tmp, BccMessage):
                messages.append(tmp)
            elif isinstance(tmp, Iterable):
                messages += tmp

        return messages

    def __merge_observations(self, observations: List[Observation]) -> Observation:
        assert len(observations) > 1

        observations[-1].merge_action_result_with_previous_observations(observations=observations[:-1])

        return observations[-1]

    def cycle(self) -> None:
        ActorBehaviourDebugger.debug()

        observation, messages = self.perceive()

        self.get_mind().revise(observation=observation, messages=messages)

        self.get_mind().decide()

        actions_to_attempt: Tuple[VWAction] = self.get_mind().execute()

        self.__attempt_actions(actions=actions_to_attempt)

    def __attempt_actions(self, actions: Tuple[VWAction]) -> None:
        for action in actions:
            self.get_mind().get_surrogate().update_effort(increment=action.get_effort())

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
