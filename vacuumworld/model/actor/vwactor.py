from typing import List, Tuple, Iterable, cast
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.elements.actor import Actor
from pystarworldsturbo.elements.sensor import Sensor
from pystarworldsturbo.elements.actuator import Actuator

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
    def __init__(self, mind: VWMind, sensors: List[VWSensor]=[], actuators: List[VWActuator]=[]) -> None:
        super(VWActor, self).__init__(mind=mind, sensors=[s for s in sensors if isinstance(s, Sensor)], actuators=[a for a in actuators if isinstance(a, Actuator)])

    def get_mind(self) -> VWMind:
        '''
        Returns the `VWMind` of this `VWActor`.
        '''
        return cast(VWMind, super(VWActor, self).get_mind())

    def get_listening_sensor(self) -> PyOptional[VWListeningSensor]:
        '''
        Return a `PyOptional` wrapping the `VWListeningSensor` of this `VWActor` if any, otherwise returns an empty `PyOptional`.
        '''
        return super(VWActor, self).get_listening_sensor().filter(lambda s: isinstance(s, VWListeningSensor)).map(lambda s: cast(VWListeningSensor, s))

    def get_observation_sensor(self) -> PyOptional[VWObservationSensor]:
        '''
        Returns a `PyOptional` wrapping the `VWObservationSensor` of this `VWActor` if any, otherwise returns an empty `PyOptional`.
        '''
        return super(VWActor, self).get_sensor_for(event_type=VWObservation).filter(lambda s: isinstance(s, VWObservationSensor)).map(lambda s: cast(VWObservationSensor, s))

    def get_physical_actuator(self) -> PyOptional[VWActuator]:
        '''
        Abstract method to be implemented by subclasses.

        It should return a `PyOptional` wrapping the `VWActuator` of this `VWActor` that is responsible for the execution of each `VWPhysicalAction`, or an empty `PyOptional` if no such `VWActuator` exists.
        '''

        raise NotImplementedError()

    def get_communicative_actuator(self) -> PyOptional[VWCommunicativeActuator]:
        '''
        Returns a `PyOptional` wrapping the `VWCommunicativeActuator` of this `VWActor` if any, otherwise returns an empty `PyOptional`.
        '''
        return super(VWActor, self).get_actuator_for(event_type=VWSpeakAction).filter(lambda a: isinstance(a, VWCommunicativeActuator)).map(lambda a: cast(VWCommunicativeActuator, a)).filter(lambda a: a.is_subscribed_to(event_type=VWBroadcastAction))

    def test_get_percepts(self) -> Tuple[VWObservation, Iterable[BccMessage]]:
        '''
        WARNING: this method is only used for testing purposes. It must be public.
        '''
        return self.__get_percepts()

    def __get_percepts(self) -> Tuple[VWObservation, Iterable[BccMessage]]:
        '''
        Returns the `List[Observation]` and the `List[BccMessage]` that are available for this `VWActor` during this cycle.
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
        observation_sensor: VWObservationSensor = self.get_observation_sensor().or_else_raise(VWPerceptionException("No sensor found for {}.".format(VWObservation)))

        # There can be more than one `VWObservation` if more than one `VWAction` has been attempted.
        while observation_sensor.has_perception():
            observations.append(observation_sensor.source().or_else_raise())

        return observations

    def __fetch_messages(self) -> List[BccMessage]:
        messages: List[BccMessage] = []

        listening_sensor: PyOptional[VWListeningSensor] = self.get_listening_sensor()

        if listening_sensor.is_present():
            while listening_sensor.get().has_perception():
                messages += [m for m in listening_sensor.get().source()]

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
        observation, messages = self.__get_percepts()

        # Stores the perceptions into the mind.
        self.get_mind().perceive(observation=observation, messages=messages)

        # Revise the internal state/beliefs based on the perceptions.
        self.get_mind().revise()

        # Decide the next `VWAction` or `List[VWAction]` to attempt.
        self.get_mind().decide()

        # Attempt the execution of the `List[VWAction]` decided by the mind.
        actions_to_attempt: List[VWAction] = self.get_mind().execute()

        # Attempt `List[VWAction]`.
        self.__attempt_actions(actions=actions_to_attempt)

    def __attempt_actions(self, actions: List[VWAction]) -> None:
        for action in actions:
            self.get_mind().get_surrogate().update_effort(increment=action.get_effort())

            action.set_actor_id(self.get_id())

            if isinstance(action, VWPhysicalAction):
                self.get_physical_actuator().or_else_raise(VWActionAttemptException("No actuator found for {}.".format(type(action)))).sink(action=action)
            elif isinstance(action, VWCommunicativeAction):
                self.get_communicative_actuator().or_else_raise(VWActionAttemptException("No actuator found for {}.".format(type(action)))).sink(action=action)
            else:
                raise VWActionAttemptException("Unsupported action type {}.".format(type(action)))
