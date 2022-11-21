from typing import List, Tuple, Iterable, Union, Optional

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.elements.actor import Actor

from .vwactor_behaviour_debugger import VWActorBehaviourDebugger
from .mind.vwactor_mind import VWMind
from .appendices.vwsensors import VWSensor, VWListeningSensor, VWObservationSensor
from .appendices.vwactuators import VWActuator, VWCommunicativeActuator
from ..actions.vwactions import VWAction, VWPhysicalAction, VWCommunicativeAction
from ..actions.vwspeak_action import VWSpeakAction
from ..actions.vwbroadcast_action import VWBroadcastAction
from ...common.vwobservation import VWObservation
from ...common.vwexceptions import VWActionAttemptException, VWPerceptionException


class VWActor(Actor):
    '''
    This abstract class specifies the actors in the VacuumWorld universe.
    '''
    def __init__(self, mind: VWMind, sensors: List[VWSensor], actuators: List[VWActuator]) -> None:
        super(VWActor, self).__init__(mind=mind, sensors=sensors, actuators=actuators)

    def get_mind(self) -> VWMind:
        '''
        Returns the `VWMind` of this `VWActor`.
        '''
        return super(VWActor, self).get_mind()

    def get_listening_sensor(self) -> Optional[VWListeningSensor]:
        '''
        Return the `VWListeningSensor` of this `VWActor` if any, `None` otherwise.
        '''
        return super(VWActor, self).get_listening_sensor()

    def get_observation_sensor(self) -> Optional[VWObservationSensor]:
        '''
        Returns the `VWObservationSensor` of this `VWActor` if any, `None` otherwise.
        '''
        return super(VWActor, self).get_sensor_for(event_type=VWObservation)

    def get_physical_actuator(_) -> Optional[VWActuator]:
        '''
        Abstract method to be implemented by subclasses.

        It should return the `VWActuator` of this `VWActor` that is responsible for the execution of each `VWPhysicalAction`.
        '''

        raise NotImplementedError()

    def get_communicative_actuator(self) -> Optional[VWCommunicativeActuator]:
        '''
        Returns the `VWCommunicativeActuator` of this `VWActor` if any, `None` otherwise.
        '''
        candidate: VWCommunicativeActuator = super(VWActor, self).get_actuator_for(event_type=VWSpeakAction)

        if candidate:
            assert candidate.is_subscribed_to(event_type=VWBroadcastAction)

            return candidate
        else:
            return None

    def perceive(self) -> Tuple[VWObservation, Iterable[BccMessage]]:
        '''
        Performs the `List[Observation]` and the `List[BccMessage]` that are available for this `VWActor` during this cycle.
        '''
        observations: List[VWObservation] = self.__fetch_observations()
        messages: List[BccMessage] = self.__fetch_messages()

        assert len(observations) > 0

        if len(observations) > 1:
            return self.__merge_observations(observations), messages
        else:
            return observations[0], messages

    def __fetch_observations(self) -> List[VWObservation]:
        observations: List[VWObservation] = []
        observation_sensor: VWObservationSensor = self.get_observation_sensor()

        if not observation_sensor:
            raise VWPerceptionException("No sensor found for {}.".format(VWObservation))

        # There can be more than one `VWObservation` if more than one `VWAction` has been attempted.
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

    def __merge_observations(self, observations: List[VWObservation]) -> VWObservation:
        assert len(observations) > 1

        observations[-1].merge_action_result_with_previous_observations(observations=observations[:-1])

        return observations[-1]

    def cycle(self) -> None:
        '''
        Cycles the `VWActor`.

        * `perceive()`
        * `revise()`
        * `decide()`
        * `execute()`
        '''
        # If debug is disabled, this call will do nothing.
        VWActorBehaviourDebugger.debug()

        # Fetch the perceptions.
        observation, messages = self.perceive()

        # Revise the internal state/beliefs based on the perceptions.
        self.get_mind().revise(observation=observation, messages=messages)

        # Decide the next `VWAction` or `Tuple[VWAction]` to attempt.
        self.get_mind().decide()

        # Attempt the execution of the `VWAction` or `Tuple[VWAction]`.
        self.execute()

    def execute(self) -> None:
        '''
        Attempts the execution of the `VWAction` or `Tuple[VWAction]` that has been decided by the `VWMind`.
        '''
        # Fetch the `VWAction` or `Tuple[VWAction]` to attempt.
        actions_to_attempt: Tuple[VWAction] = self.get_mind().execute()

        # Attempt the `VWAction` or `Tuple[VWAction]`.
        self.__attempt_actions(actions=actions_to_attempt)

    def __attempt_actions(self, actions: Tuple[VWAction]) -> None:
        for action in actions:
            self.get_mind().get_surrogate().update_effort(increment=action.get_effort())

            action.set_actor_id(self.get_id())

            actuator: VWActuator = None

            if isinstance(action, VWPhysicalAction):
                actuator = self.get_physical_actuator()
            elif isinstance(action, VWCommunicativeAction):
                actuator = self.get_communicative_actuator()

            if not actuator:
                raise VWActionAttemptException("No actuator found for {}.".format(type(action)))
            else:
                actuator.sink(action=action)
