#!/usr/bin/env python3

from unittest import main, TestCase
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
from vacuumworld.model.actor.vwusermind import VWUserMind
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


class TestActors(TestCase):
    def test_agent_mind_creation(self) -> None:
        surrogate: HystereticMind = HystereticMind()
        mind: VWMind = VWMind(surrogate=surrogate)

        self.assertEqual(surrogate.__class__, mind.get_surrogate().__class__)

    def test_user_mind_creation(self) -> None:
        easy_surrogate: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty.easy)
        hard_surrogate: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty.hard)
        easy_mind: VWUserMind = VWUserMind(surrogate=easy_surrogate)
        hard_mind: VWUserMind = VWUserMind(surrogate=hard_surrogate)

        self.assertEqual(easy_surrogate.get_difficulty_level(), UserDifficulty.easy)
        self.assertEqual(hard_surrogate.get_difficulty_level(), UserDifficulty.hard)
        self.assertEqual(easy_mind.get_surrogate().get_difficulty_level(), UserDifficulty.easy)
        self.assertEqual(hard_mind.get_surrogate().get_difficulty_level(), UserDifficulty.hard)

    def test_cleaning_agent_creation(self) -> None:
        surrogate: HystereticMind = HystereticMind()
        mind: VWMind = VWMind(surrogate=surrogate)

        for colour in [Colour.white, Colour.green, Colour.orange]:
            for orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]:
                agent: VWCleaningAgent = VWCleaningAgent(mind=mind)
                appearance: VWActorAppearance = VWActorAppearance(colour=colour, orientation=orientation, actor_id=agent.get_id(), progressive_id=agent.get_progressive_id())
                factory_agent, factory_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, mind_surrogate=surrogate, orientation=orientation)

                # Test agent body vs. appearance
                self.assertEqual(agent.get_id(), appearance.get_id())
                self.assertEqual(factory_agent.get_id(), factory_agent_appearance.get_id())
                self.assertEqual(agent.get_progressive_id(), appearance.get_progressive_id())
                self.assertEqual(factory_agent.get_progressive_id(), factory_agent_appearance.get_progressive_id())

                # Test agent appearance
                self.assertEqual(appearance.get_colour(), colour)
                self.assertEqual(factory_agent_appearance.get_colour(), colour)
                self.assertEqual(appearance.get_orientation(), orientation)
                self.assertEqual(factory_agent_appearance.get_orientation(), orientation)

                # Test sensors and actuators
                for a in (agent, factory_agent):
                    self.assertEqual(len(a.get_sensors()), 2)
                    self.assertEqual(len(a.get_actuators()), 2)
                    self.assertIsNotNone(a.get_listening_sensor())
                    self.assertEqual(a.get_listening_sensor(), a.get_sensor_for(event_type=BccMessage))
                    self.assertIsNotNone(a.get_observation_sensor())
                    self.assertEqual(a.get_observation_sensor(), a.get_sensor_for(event_type=Observation))
                    self.assertNotEqual(a.get_listening_sensor(), a.get_observation_sensor())
                    self.assertIsNotNone(a.get_communicative_actuator())
                    self.assertEqual(a.get_communicative_actuator(), a.get_actuator_for(event_type=VWBroadcastAction))
                    self.assertEqual(a.get_communicative_actuator(), a.get_actuator_for(event_type=VWSpeakAction))
                    self.assertIsNotNone(a.get_physical_actuator())
                    self.assertEqual(a.get_physical_actuator(), a.get_actuator_for(event_type=VWIdleAction))
                    self.assertEqual(a.get_physical_actuator(), a.get_actuator_for(event_type=VWMoveAction))
                    self.assertEqual(a.get_physical_actuator(), a.get_actuator_for(event_type=VWCleanAction))
                    self.assertEqual(a.get_physical_actuator(), a.get_actuator_for(event_type=VWTurnAction))
                    self.assertIsNone(a.get_actuator_for(event_type=VWDropAction))
                    self.assertNotEqual(a.get_communicative_actuator(), a.get_physical_actuator())

    def test_user_creation(self) -> None:
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
                self.assertEqual(user.get_id(), appearance.get_id())
                self.assertEqual(factory_user.get_id(), factory_user_appearance.get_id())
                self.assertEqual(user.get_progressive_id(), appearance.get_progressive_id())
                self.assertEqual(factory_user.get_progressive_id(), factory_user_appearance.get_progressive_id())

                # Test user appearance
                self.assertEqual(appearance.get_colour(), Colour.user)
                self.assertEqual(factory_user_appearance.get_colour(), Colour.user)
                self.assertEqual(appearance.get_orientation(), orientation)
                self.assertEqual(factory_user_appearance.get_orientation(), orientation)

                # Test sensors and actuators
                for u in (user, factory_user):
                    self.assertEqual(len(u.get_sensors()), 2)
                    self.assertEqual(len(u.get_actuators()), 2)
                    self.assertIsNotNone(u.get_listening_sensor())
                    self.assertEqual(u.get_listening_sensor(), u.get_sensor_for(event_type=BccMessage))
                    self.assertIsNotNone(u.get_observation_sensor())
                    self.assertEqual(u.get_observation_sensor(), u.get_sensor_for(event_type=Observation))
                    self.assertNotEqual(u.get_listening_sensor(), u.get_observation_sensor())
                    self.assertIsNotNone(u.get_communicative_actuator())
                    self.assertEqual(u.get_communicative_actuator(), u.get_actuator_for(event_type=VWBroadcastAction))
                    self.assertEqual(u.get_communicative_actuator(), u.get_actuator_for(event_type=VWSpeakAction))
                    self.assertIsNotNone(u.get_physical_actuator())
                    self.assertEqual(u.get_physical_actuator(), u.get_actuator_for(event_type=VWIdleAction))
                    self.assertEqual(u.get_physical_actuator(), u.get_actuator_for(event_type=VWMoveAction))
                    self.assertEqual(u.get_physical_actuator(), u.get_actuator_for(event_type=VWDropAction))
                    self.assertEqual(u.get_physical_actuator(), u.get_actuator_for(event_type=VWTurnAction))
                    self.assertIsNone(u.get_actuator_for(event_type=VWCleanAction))
                    self.assertNotEqual(u.get_communicative_actuator(), u.get_physical_actuator())


if __name__ == "__main__":
    main()
