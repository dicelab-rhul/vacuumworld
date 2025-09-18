#!/usr/bin/env python3

from unittest import main, TestCase

from pystarworldsturbo.common.message import BccMessage

from vacuumworld.common.vwuser_difficulty import VWUserDifficulty
from vacuumworld.model.actor.vwactor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.model.actor.appearance.vwactor_appearance import VWActorAppearance
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.model.actor.mind.vwactor_mind import VWMind
from vacuumworld.model.actor.mind.vwuser_mind import VWUserMind
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.model.actor.mind.surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from vacuumworld.model.actor.vwagent import VWCleaningAgent
from vacuumworld.model.actor.vwuser import VWUser
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwspeak_action import VWSpeakAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwclean_action import VWCleanAction
from vacuumworld.model.actions.vwdrop_action import VWDropAction


class TestActors(TestCase):
    '''
    This class tests:
    * The construction of `VWUserMindSurrogate` objects.
    * The construction of objects whose class is a subclass of `VWActorMindSurrogate` (in this case, `VWHystereticMindSurrogate`).
    * The construction of `VWMind` and `VWUserMind` objects from `VWHystereticMindSurrogate` and `VWUsermindSurrogate` objects respectively.
    * The constructon of `VWCleaningAgent` and `VWUser` via `VWCleaningAgentsFactory` and `VWUsersFactory` respectively.
    '''
    def test_agent_mind_creation(self) -> None:
        '''
        Tests the creation of `VWHystereticMindSurrogate` and `VWMind` objects.
        '''
        surrogate: VWHystereticMindSurrogate = VWHystereticMindSurrogate()
        mind: VWMind = VWMind(surrogate=surrogate)

        self.assertEqual(surrogate.__class__, mind.get_surrogate().__class__)

    def test_user_mind_creation(self) -> None:
        '''
        Tests the creation of `VWUserMindSurrogate` and `VWUserMind` objects.
        '''
        easy_surrogate: VWUserMindSurrogate = VWUserMindSurrogate(difficulty_level=VWUserDifficulty.easy)
        hard_surrogate: VWUserMindSurrogate = VWUserMindSurrogate(difficulty_level=VWUserDifficulty.hard)
        easy_mind: VWUserMind = VWUserMind(surrogate=easy_surrogate)
        hard_mind: VWUserMind = VWUserMind(surrogate=hard_surrogate)

        self.assertEqual(easy_surrogate.get_difficulty_level(), VWUserDifficulty.easy)
        self.assertEqual(hard_surrogate.get_difficulty_level(), VWUserDifficulty.hard)
        self.assertEqual(easy_mind.get_surrogate().get_difficulty_level(), VWUserDifficulty.easy)
        self.assertEqual(hard_mind.get_surrogate().get_difficulty_level(), VWUserDifficulty.hard)

    def test_cleaning_agent_creation(self) -> None:
        '''
        Tests the creation of `VWCleaningAgent` objects via `VWCleaningAgentsFactory`.
        '''
        surrogate: VWHystereticMindSurrogate = VWHystereticMindSurrogate()
        mind: VWMind = VWMind(surrogate=surrogate)

        for colour in [VWColour.white, VWColour.green, VWColour.orange]:
            for orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]:
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
                    self.assertTrue(a.get_listening_sensor().is_present())
                    self.assertEqual(a.get_listening_sensor().or_else_raise(), a.get_sensor_for(event_type=BccMessage).or_else_raise())
                    self.assertTrue(a.get_observation_sensor().is_present())
                    self.assertEqual(a.get_observation_sensor().or_else_raise(), a.get_sensor_for(event_type=VWObservation).or_else_raise())
                    self.assertNotEqual(a.get_listening_sensor().or_else_raise(), a.get_observation_sensor().or_else_raise())
                    self.assertTrue(a.get_communicative_actuator().is_present())
                    self.assertEqual(a.get_communicative_actuator().or_else_raise(), a.get_actuator_for(event_type=VWBroadcastAction).or_else_raise())
                    self.assertEqual(a.get_communicative_actuator().or_else_raise(), a.get_actuator_for(event_type=VWSpeakAction).or_else_raise())
                    self.assertTrue(a.get_physical_actuator().is_present())
                    self.assertEqual(a.get_physical_actuator().or_else_raise(), a.get_actuator_for(event_type=VWIdleAction).or_else_raise())
                    self.assertEqual(a.get_physical_actuator().or_else_raise(), a.get_actuator_for(event_type=VWMoveAction).or_else_raise())
                    self.assertEqual(a.get_physical_actuator().or_else_raise(), a.get_actuator_for(event_type=VWCleanAction).or_else_raise())
                    self.assertEqual(a.get_physical_actuator().or_else_raise(), a.get_actuator_for(event_type=VWTurnAction).or_else_raise())
                    self.assertTrue(a.get_actuator_for(event_type=VWDropAction).is_empty())
                    self.assertNotEqual(a.get_communicative_actuator().or_else_raise(), a.get_physical_actuator().or_else_raise())

    def test_user_creation(self) -> None:
        '''
        Tests the creation of `VWUser` objects via `VWUsersFactory`.
        '''
        easy_surrogate: VWUserMindSurrogate = VWUserMindSurrogate(difficulty_level=VWUserDifficulty.easy)
        hard_surrogate: VWUserMindSurrogate = VWUserMindSurrogate(difficulty_level=VWUserDifficulty.hard)
        easy_mind: VWUserMind = VWUserMind(surrogate=easy_surrogate)
        hard_mind: VWUserMind = VWUserMind(surrogate=hard_surrogate)

        for mind, level in {easy_mind: VWUserDifficulty.easy, hard_mind: VWUserDifficulty.hard}.items():
            for orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]:
                user: VWUser = VWUser(mind=mind)
                appearance: VWActorAppearance = VWActorAppearance(colour=VWColour.user, orientation=orientation, actor_id=user.get_id(), progressive_id=user.get_progressive_id())
                factory_user, factory_user_appearance = VWUsersFactory.create_user(difficulty_level=level, orientation=orientation)

                # Test user appearance
                self.assertEqual(user.get_id(), appearance.get_id())
                self.assertEqual(factory_user.get_id(), factory_user_appearance.get_id())
                self.assertEqual(user.get_progressive_id(), appearance.get_progressive_id())
                self.assertEqual(factory_user.get_progressive_id(), factory_user_appearance.get_progressive_id())

                # Test user appearance
                self.assertEqual(appearance.get_colour(), VWColour.user)
                self.assertEqual(factory_user_appearance.get_colour(), VWColour.user)
                self.assertEqual(appearance.get_orientation(), orientation)
                self.assertEqual(factory_user_appearance.get_orientation(), orientation)

                # Test sensors and actuators
                for u in (user, factory_user):
                    self.assertEqual(len(u.get_sensors()), 2)
                    self.assertEqual(len(u.get_actuators()), 2)
                    self.assertTrue(u.get_listening_sensor().is_present())
                    self.assertEqual(u.get_listening_sensor().or_else_raise(), u.get_sensor_for(event_type=BccMessage).or_else_raise())
                    self.assertTrue(u.get_observation_sensor().is_present())
                    self.assertEqual(u.get_observation_sensor().or_else_raise(), u.get_sensor_for(event_type=VWObservation).or_else_raise())
                    self.assertNotEqual(u.get_listening_sensor().or_else_raise(), u.get_observation_sensor().or_else_raise())
                    self.assertTrue(u.get_communicative_actuator().is_present())
                    self.assertEqual(u.get_communicative_actuator().or_else_raise(), u.get_actuator_for(event_type=VWBroadcastAction).or_else_raise())
                    self.assertEqual(u.get_communicative_actuator().or_else_raise(), u.get_actuator_for(event_type=VWSpeakAction).or_else_raise())
                    self.assertTrue(u.get_physical_actuator().is_present())
                    self.assertEqual(u.get_physical_actuator().or_else_raise(), u.get_actuator_for(event_type=VWIdleAction).or_else_raise())
                    self.assertEqual(u.get_physical_actuator().or_else_raise(), u.get_actuator_for(event_type=VWMoveAction).or_else_raise())
                    self.assertEqual(u.get_physical_actuator().or_else_raise(), u.get_actuator_for(event_type=VWDropAction).or_else_raise())
                    self.assertEqual(u.get_physical_actuator().or_else_raise(), u.get_actuator_for(event_type=VWTurnAction).or_else_raise())
                    self.assertTrue(u.get_actuator_for(event_type=VWCleanAction).is_empty())
                    self.assertNotEqual(u.get_communicative_actuator().or_else_raise(), u.get_physical_actuator().or_else_raise())


if __name__ == "__main__":
    main()
