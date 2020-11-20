#!/usr/bin/env python3

from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld.model.actor.user_difficulty import UserDifficulty
from vacuumworld.model.actor.actor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.common.colour import Colour
from vacuumworld.common.observation import Observation
from vacuumworld.model.actor.vwactormind import VWMind
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actor.user_mind_surrogate import UserMindSurrogate
from vacuumworld.model.actor.vwagent import VWCleaningAgent
from vacuumworld.model.actor.vwuser import VWUser
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.speak_action import VWSpeakAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.clean_action import VWCleanAction
from vacuumworld.model.actions.drop_action import VWDropAction



class HystereticMind(ActorMindSurrogate):
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        ignore(self)

        return VWIdleAction()


def test_agent_mind_creation() -> None:
    surrogate: HystereticMind = HystereticMind()
    _: VWMind = VWMind(surrogate=surrogate)


def test_user_mind_creation() -> None:
    easy_surrogate: HystereticMind = UserMindSurrogate(difficulty_level=UserDifficulty.easy)
    hard_surrogate: HystereticMind = UserMindSurrogate(difficulty_level=UserDifficulty.hard)
    easy_mind: VWMind = VWMind(surrogate=easy_surrogate)
    hard_mind: VWMind = VWMind(surrogate=hard_surrogate)

    assert easy_surrogate.get_difficulty_level() == UserDifficulty.easy
    assert hard_surrogate.get_difficulty_level() == UserDifficulty.hard
    assert easy_mind.get_surrogate().get_difficulty_level() == UserDifficulty.easy
    assert hard_mind.get_surrogate().get_difficulty_level() == UserDifficulty.hard


def test_cleaning_agent_creation() -> None:
    surrogate: HystereticMind = HystereticMind()
    mind: VWMind = VWMind(surrogate=surrogate)

    for colour in [Colour.white, Colour.green, Colour.orange]:
        for orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]:
            agent: VWCleaningAgent = VWCleaningAgent(mind=mind)
            appearance: VWActorAppearance = VWActorAppearance(colour=colour, orientation=orientation, actor_id=agent.get_id(), progressive_id=agent.get_progressive_id())
            factory_agent, factory_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, mind_surrogate=surrogate, orientation=orientation)

            # Test agent body vs. appearance
            assert agent.get_id() == appearance.get_id()
            assert factory_agent.get_id() == factory_agent_appearance.get_id()
            assert agent.get_progressive_id() == appearance.get_progressive_id()
            assert factory_agent.get_progressive_id() == factory_agent_appearance.get_progressive_id()
            
            # Test agent appearance
            assert appearance.name == "A-" + appearance.get_progressive_id() and factory_agent_appearance.name == "A-" + factory_agent_appearance.get_progressive_id()
            assert appearance.get_colour() == colour and factory_agent_appearance.get_colour() == colour
            assert appearance.colour == colour and factory_agent_appearance.colour == colour
            assert appearance.get_orientation() == orientation and factory_agent_appearance.get_orientation() == orientation
            assert appearance.orientation == orientation and factory_agent_appearance.orientation == orientation
            
            # Test sensors and actuators
            for a in (agent, factory_agent):
                assert len(a.get_sensors()) == 2 and len(a.get_actuators()) == 2
                assert a.get_listening_sensor() is not None
                assert a.get_listening_sensor() == a.get_sensor_for(event_type=BccMessage)
                assert a.get_observation_sensor() is not None
                assert a.get_observation_sensor() == a.get_sensor_for(event_type=Observation)
                assert a.get_listening_sensor() != a.get_observation_sensor()
                assert a.get_communicative_actuator() is not None
                assert a.get_communicative_actuator() == a.get_actuator_for(event_type=VWBroadcastAction)
                assert a.get_communicative_actuator() == a.get_actuator_for(event_type=VWSpeakAction)
                assert a.get_physical_actuator() is not None
                assert a.get_physical_actuator() == a.get_actuator_for(event_type=VWIdleAction)
                assert a.get_physical_actuator() == a.get_actuator_for(event_type=VWMoveAction)
                assert a.get_physical_actuator() == a.get_actuator_for(event_type=VWCleanAction)
                assert a.get_physical_actuator() == a.get_actuator_for(event_type=VWTurnAction)
                assert a.get_actuator_for(event_type=VWDropAction) is None
                assert a.get_communicative_actuator() != a.get_physical_actuator()


def test_user_creation() -> None:
    easy_surrogate: HystereticMind = UserMindSurrogate(difficulty_level=UserDifficulty.easy)
    hard_surrogate: HystereticMind = UserMindSurrogate(difficulty_level=UserDifficulty.hard)
    easy_mind: VWMind = VWMind(surrogate=easy_surrogate)
    hard_mind: VWMind = VWMind(surrogate=hard_surrogate)

    for mind, level in {easy_mind: UserDifficulty.easy, hard_mind: UserDifficulty.hard}.items():
        for orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]:
            user: VWUser = VWUser(mind=mind)
            appearance: VWActorAppearance = VWActorAppearance(colour=Colour.user, orientation=orientation, actor_id=user.get_id(), progressive_id=user.get_progressive_id())
            factory_user, factory_user_appearance = VWUsersFactory.create_user(difficulty_level=level, orientation=orientation)

            # Test user appearance
            assert user.get_id() == appearance.get_id()
            assert factory_user.get_id() == factory_user_appearance.get_id()
            assert user.get_progressive_id() == appearance.get_progressive_id()
            assert factory_user.get_progressive_id() == factory_user_appearance.get_progressive_id()
            
            # Test user appearance
            assert appearance.name == "U-" + appearance.get_progressive_id() and factory_user_appearance.name == "U-" + factory_user_appearance.get_progressive_id()
            assert appearance.get_colour() == Colour.user and factory_user_appearance.get_colour() == Colour.user
            assert appearance.colour == Colour.user and factory_user_appearance.colour == Colour.user
            assert appearance.get_orientation() == orientation and factory_user_appearance.get_orientation() == orientation
            assert appearance.orientation == orientation and factory_user_appearance.orientation == orientation

            # Test sensors and actuators
            for u in (user, factory_user):
                assert len(u.get_sensors()) == 2 and len(u.get_actuators()) == 2
                assert u.get_listening_sensor() is not None
                assert u.get_listening_sensor() == u.get_sensor_for(event_type=BccMessage)
                assert u.get_observation_sensor() is not None
                assert u.get_observation_sensor() == u.get_sensor_for(event_type=Observation)
                assert u.get_listening_sensor() != u.get_observation_sensor()
                assert u.get_communicative_actuator() is not None
                assert u.get_communicative_actuator() == u.get_actuator_for(event_type=VWBroadcastAction)
                assert u.get_communicative_actuator() == u.get_actuator_for(event_type=VWSpeakAction)
                assert u.get_physical_actuator() is not None
                assert u.get_physical_actuator() == u.get_actuator_for(event_type=VWIdleAction)
                assert u.get_physical_actuator() == u.get_actuator_for(event_type=VWMoveAction)
                assert u.get_physical_actuator() == u.get_actuator_for(event_type=VWDropAction)
                assert u.get_physical_actuator() == u.get_actuator_for(event_type=VWTurnAction)
                assert u.get_actuator_for(event_type=VWCleanAction) is None
                assert u.get_communicative_actuator() != u.get_physical_actuator()


def test_all() -> None:
    test_agent_mind_creation()
    test_user_mind_creation()
    test_cleaning_agent_creation()
    test_user_creation()


if __name__ == "__main__":
    test_all()
