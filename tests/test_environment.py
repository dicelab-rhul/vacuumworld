#!/usr/bin/env python3

from unittest import main, TestCase
from random import randint

from vacuumworld import VacuumWorld
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.common.vwuser_difficulty import VWUserDifficulty
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.model.actor.vwactor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.model.dirt.vwdirt_appearance import VWDirtAppearance
from vacuumworld.model.dirt.vwdirt import VWDirt
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.vwconfig_manager import VWConfigManager


class TestEnvironment(TestCase):
    '''
    This class tests the creation of `VWAmbient` and `VWEnvironment` objects with various grid sizes and various amounts of `VWActor` and `VWDirt` objects.
    '''
    def __init__(self, args) -> None:
        super(TestEnvironment, self).__init__(args)

        self.__config: dict = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)

    def test_default_sized_empty_env(self) -> None:
        '''
        Tests the creation of an empty `VWEnvironment` object, with the default grid size.
        '''
        self.__test_empty_env(custom_grid_size=False)

    def test_custom_sized_empty_env(self) -> None:
        '''
        Tests the creation of an empty `VWEnvironment` object, with a custom random grid size.
        '''
        self.__test_empty_env(custom_grid_size=True)

    def __test_empty_env(self, custom_grid_size: bool) -> None:
        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=self.__config)

        self.assertEqual(env.get_ambient().get_grid_dim(), grid_size)
        self.assertEqual(len(env.get_ambient().get_grid()), grid_size ** 2)
        self.assertEqual(len(env.get_actors()), 0)
        self.assertEqual(len(env.get_actors_list()), 0)
        self.assertEqual(len(env.get_passive_bodies()), 0)
        self.assertEqual(len(env.get_passive_bodies_list()), 0)

    def test_default_sized_env_with_agents(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with the default grid size, and a `VWCleaningAgent` for each `VWColour` (except for `VWColour.user`).
        '''
        self.__test_env_with_cleaning_agents(custom_grid_size=False)

    def test_custom_sized_env_with_agents(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with a custom random grid size, and a `VWCleaningAgent` for each `VWColour` (except for `VWColour.user`).
        '''
        self.__test_env_with_cleaning_agents(custom_grid_size=True)

    def __test_env_with_cleaning_agents(self, custom_grid_size: bool) -> None:
        green_agent_orientation: VWOrientation = VWOrientation.random()
        orange_agent_orientation: VWOrientation = VWOrientation.random()
        white_agent_orientation: VWOrientation = VWOrientation.random()

        green_agent, green_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.green, orientation=green_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        orange_agent, orange_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.orange, orientation=orange_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        white_agent, white_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.white, orientation=white_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())

        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=self.__config)

        self.assertEqual(env.get_ambient().get_grid_dim(), grid_size)
        self.assertEqual(len(env.get_ambient().get_grid()), grid_size ** 2)

        env.add_actor(actor=green_agent)
        env.add_actor(actor=orange_agent)
        env.add_actor(actor=white_agent)

        green_agent_coord, orange_agent_coord, white_agent_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=3, grid_size=grid_size)

        env.get_ambient().get_grid()[green_agent_coord] = VWLocation(coord=green_agent_coord, actor_appearance=green_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[orange_agent_coord] = VWLocation(coord=orange_agent_coord, actor_appearance=orange_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[white_agent_coord] = VWLocation(coord=white_agent_coord, actor_appearance=white_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=white_agent_coord, grid_size=grid_size))

        self.assertEqual(len(env.get_actors()), 3)
        self.assertEqual(len(env.get_actors_list()), 3)
        self.assertTrue(env.get_ambient().get_grid()[green_agent_coord].has_cleaning_agent())
        self.assertTrue(env.get_ambient().get_grid()[orange_agent_coord].has_cleaning_agent())
        self.assertTrue(env.get_ambient().get_grid()[white_agent_coord].has_cleaning_agent())

        # For the tests on the actor appearance, go to test_location_and_coordinates.py, and test_actors.py.

    def test_default_sized_env_with_dirts(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with the default grid size, and a `VWDirt` for each `VWColour` (except for `VWColour.white`, and `VWColour.user`).
        '''
        self.__test_env_with_dirts(custom_grid_size=False)

    def test_custom_sized_env_with_dirts(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with a custom random grid size, and a `VWDirt` for each `VWColour` (except for `VWColour.white`, and `VWColour.user`).
        '''
        self.__test_env_with_dirts(custom_grid_size=True)

    def __test_env_with_dirts(self, custom_grid_size: bool) -> None:
        green_dirt: VWDirt = VWDirt(colour=VWColour.green)
        green_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=green_dirt.get_id(), progressive_id=green_dirt.get_progressive_id(), colour=VWColour.green)

        orange_dirt: VWDirt = VWDirt(colour=VWColour.orange)
        orange_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=orange_dirt.get_id(), progressive_id=orange_dirt.get_progressive_id(), colour=VWColour.orange)

        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=self.__config)

        self.assertEqual(env.get_ambient().get_grid_dim(), grid_size)
        self.assertEqual(len(env.get_ambient().get_grid()), grid_size ** 2)

        env.add_passive_body(passive_body=green_dirt)
        env.add_passive_body(passive_body=orange_dirt)

        green_dirt_coord, orange_dirt_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=2, grid_size=grid_size)

        env.get_ambient().get_grid()[green_dirt_coord] = VWLocation(coord=green_dirt_coord, dirt_appearance=green_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_dirt_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[orange_dirt_coord] = VWLocation(coord=orange_dirt_coord, dirt_appearance=orange_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_dirt_coord, grid_size=grid_size))

        self.assertEqual(len(env.get_passive_bodies()), 2)
        self.assertEqual(len(env.get_passive_bodies_list()), 2)
        self.assertTrue(env.get_ambient().get_grid()[green_dirt_coord].has_dirt())
        self.assertTrue(env.get_ambient().get_grid()[orange_dirt_coord].has_dirt())

        # For the tests on the dirt appearance, go to test_location_and_coordinates.py, and test_dirt.py.

    def test_default_sized_env_with_user(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with the default grid size, and a `VWUser` object.
        '''
        self.__test_env_with_user(custom_grid_size=False)

    def test_custom_sized_env_with_user(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with a custom random grid size, and a `VWUser` object.
        '''
        self.__test_env_with_user(custom_grid_size=True)

    def __test_env_with_user(self, custom_grid_size: bool) -> None:
        user_orientation: VWOrientation = VWOrientation.random()
        difficutly_level: VWUserDifficulty = VWUserDifficulty.random()

        user, user_appearance = VWUsersFactory.create_user(difficulty_level=difficutly_level, orientation=user_orientation)

        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=self.__config)

        self.assertEqual(env.get_ambient().get_grid_dim(), grid_size)
        self.assertEqual(len(env.get_ambient().get_grid()), grid_size ** 2)

        env.add_actor(actor=user)

        user_coord: VWCoord = VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

        env.get_ambient().get_grid()[user_coord] = VWLocation(coord=user_coord, actor_appearance=user_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=user_coord, grid_size=grid_size))

        self.assertEqual(len(env.get_actors()), 1)
        self.assertEqual(len(env.get_actors_list()), 1)
        self.assertTrue(env.get_ambient().get_grid()[user_coord].has_user())

        # For the tests on the actor appearance, go to test_location_and_coordinates.py, and test_actors.py.

    def test_default_sized_env_with_actors_and_dirts(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with the default grid size, a `VWActor` for each `VWColour`, and a `VWDirt` for each `VWColour` (except for `VWColour.white`, and `VWColour.user`).
        '''
        self.__test_env_with_actors_and_dirts(custom_grid_size=False)

    def test_custom_sized_env_with_actors_and_dirts(self) -> None:
        '''
        Tests the creation of a `VWEnvironment` object, with a custom random grid size, a `VWActor` for each `VWColour`, and a `VWDirt` for each `VWColour` (except for `VWColour.white`, and `VWColour.user`).
        '''
        self.__test_env_with_actors_and_dirts(custom_grid_size=True)

    def __test_env_with_actors_and_dirts(self, custom_grid_size: bool) -> None:
        green_agent_orientation: VWOrientation = VWOrientation.random()
        orange_agent_orientation: VWOrientation = VWOrientation.random()
        white_agent_orientation: VWOrientation = VWOrientation.random()
        user_orientation: VWOrientation = VWOrientation.random()
        difficutly_level: VWUserDifficulty = VWUserDifficulty.random()

        green_agent, green_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.green, orientation=green_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        orange_agent, orange_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.orange, orientation=orange_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        white_agent, white_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.white, orientation=white_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        user, user_appearance = VWUsersFactory.create_user(difficulty_level=difficutly_level, orientation=user_orientation)

        green_dirt: VWDirt = VWDirt(colour=VWColour.green)
        green_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=green_dirt.get_id(), progressive_id=green_dirt.get_progressive_id(), colour=VWColour.green)

        orange_dirt: VWDirt = VWDirt(colour=VWColour.orange)
        orange_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=orange_dirt.get_id(), progressive_id=orange_dirt.get_progressive_id(), colour=VWColour.orange)

        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=self.__config)

        self.assertEqual(env.get_ambient().get_grid_dim(), grid_size)
        self.assertEqual(len(env.get_ambient().get_grid()), grid_size ** 2)

        env.add_actor(actor=green_agent)
        env.add_actor(actor=orange_agent)
        env.add_actor(actor=white_agent)
        env.add_actor(actor=user)
        env.add_passive_body(passive_body=green_dirt)
        env.add_passive_body(passive_body=orange_dirt)

        green_agent_coord, orange_agent_coord, white_agent_coord, user_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=4, grid_size=grid_size)
        green_dirt_coord, orange_dirt_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=2, grid_size=grid_size)

        env.get_ambient().get_grid()[green_agent_coord] = VWLocation(coord=green_agent_coord, actor_appearance=green_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[orange_agent_coord] = VWLocation(coord=orange_agent_coord, actor_appearance=orange_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[white_agent_coord] = VWLocation(coord=white_agent_coord, actor_appearance=white_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=white_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[user_coord] = VWLocation(coord=user_coord, actor_appearance=user_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=user_coord, grid_size=grid_size))

        if green_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[green_dirt_coord].add_dirt(dirt_appearance=green_dirt_appearance)
        else:
            env.get_ambient().get_grid()[green_dirt_coord] = VWLocation(coord=green_dirt_coord, dirt_appearance=green_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_dirt_coord, grid_size=grid_size))

        if orange_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[orange_dirt_coord].add_dirt(dirt_appearance=orange_dirt_appearance)
        else:
            env.get_ambient().get_grid()[orange_dirt_coord] = VWLocation(coord=orange_dirt_coord, dirt_appearance=orange_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_dirt_coord, grid_size=grid_size))

        self.assertEqual(len(env.get_actors()), 4)
        self.assertEqual(len(env.get_actors_list()), 4)
        self.assertEqual(len(env.get_passive_bodies()), 2)
        self.assertEqual(len(env.get_passive_bodies_list()), 2)
        self.assertTrue(env.get_ambient().get_grid()[green_agent_coord].has_cleaning_agent())
        self.assertTrue(env.get_ambient().get_grid()[orange_agent_coord].has_cleaning_agent())
        self.assertTrue(env.get_ambient().get_grid()[white_agent_coord].has_cleaning_agent())
        self.assertTrue(env.get_ambient().get_grid()[user_coord].has_user())
        self.assertTrue(env.get_ambient().get_grid()[green_dirt_coord].has_dirt())
        self.assertTrue(env.get_ambient().get_grid()[orange_dirt_coord].has_dirt())

        # For the tests on the actor appearance, go to test_location_and_coordinates.py, test_actors.py, and test_dirt.py.


if __name__ == "__main__":
    main()
