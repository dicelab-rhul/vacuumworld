#!/usr/bin/env python3

from unittest import main, TestCase
from random import randint, choice
from string import ascii_letters, digits
from typing import List, Tuple

from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.actor.user_difficulty import UserDifficulty
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.model.actor.actor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.model.dirt.dirt import Dirt
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.config_manager import ConfigManager
from vacuumworld.gui.saveload import SaveStateManager

import os


class TestSaveLoad(TestCase):
    def __init__(self, args) -> None:
        super(TestSaveLoad, self).__init__(args)

        self.__save_state_manager = SaveStateManager()
        self.__config_file_name: str = "config.json"
        self.__vw_dir_name: str = "vacuumworld"
        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.__vw_dir_name, self.__config_file_name)
        self.__config_manager: ConfigManager = ConfigManager(config_file_path=self.__config_file_path)
        self.__config: dict = self.__config_manager.load_config()
        self.__default_grid_size: int = self.__config["initial_environment_dim"]
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]

    def test_save_to_file(self):
        env, _ = self.__generate_random_environment(custom_grid_size=True)
        filename: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + ".json"

        try:
            self.assertTrue(self.__save_state_manager.save_state(env=env, filename=filename))
        except AssertionError as e:
            e.args += ("We are still deleting the temporary saved state.",)

            # We rethrow the Exception, and we delete the file in the `finally` block.
            raise e
        finally:
            self.__save_state_manager.remove_saved_state(filename=filename)

    def test_load_from_file(self):
        env, _ = self.__generate_random_environment(custom_grid_size=True)
        filename: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + ".json"

        try:
            self.assertTrue(self.__save_state_manager.save_state(env=env, filename=filename))

            loaded_grid: dict = self.__save_state_manager.load_state(filename=filename)
            loaded_env: VWEnvironment = VWEnvironment.from_json(data=loaded_grid, config=self.__config)

            self.assertTrue(TestSaveLoad.__env_match(env, loaded_env))
        except AssertionError as e:
            e.args += ("We are still deleting the temporary saved state.",)

            # We rethrow the Exception, and we delete the file in the `finally` block.
            raise e
        finally:
            self.__save_state_manager.remove_saved_state(filename=filename)

    @staticmethod
    def __env_match(env1: VWEnvironment, env2: VWEnvironment) -> bool:
        assert env1 and env2

        if len(env1.get_actors_list()) != len(env2.get_actors_list()):
            return False

        if len(env1.get_passive_bodies_list()) != len(env2.get_passive_bodies_list()):
            return False

        for coord in [Coord(x, y) for x in range(env1.get_ambient().get_grid_dim()) for y in range(env1.get_ambient().get_grid_dim())]:
            if not TestSaveLoad.__compatible(loc1=env1.get_ambient().get_grid()[coord], loc2=env2.get_ambient().get_grid()[coord]):
                return False

        return True

    @staticmethod
    def __compatible(loc1: VWLocation, loc2: VWLocation) -> bool:
        assert loc1 is not None and loc2 is not None

        if loc1.get_coord() != loc2.get_coord():
            return False

        if loc1.has_cleaning_agent() and not loc2.has_cleaning_agent():
            return False

        if loc1.has_user() and not loc2.has_user():
            return False

        if loc1.has_dirt() and not loc2.has_dirt():
            return False

        if loc1.has_actor() and loc1.has_dirt():
            return loc1.get_actor_appearance().equals_except_ids(loc2.get_actor_appearance()) and loc1.get_dirt_appearance().equals_except_ids(loc2.get_dirt_appearance())
        elif loc1.has_actor():
            return loc1.get_actor_appearance().equals_except_ids(loc2.get_actor_appearance())
        elif loc1.has_dirt():
            return loc1.get_dirt_appearance().equals_except_ids(loc2.get_dirt_appearance())

        return True

    def __generate_random_environment(self, custom_grid_size: bool) -> Tuple[VWEnvironment, int]:
        green_agent_orientation: Orientation = Orientation.random()
        orange_agent_orientation: Orientation = Orientation.random()
        white_agent_orientation: Orientation = Orientation.random()
        user_orientation: Orientation = Orientation.random()
        difficutly_level: UserDifficulty = UserDifficulty.random()

        green_agent, green_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.green, orientation=green_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        orange_agent, orange_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.orange, orientation=orange_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        white_agent, white_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.white, orientation=white_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        user, user_appearance = VWUsersFactory.create_user(difficulty_level=difficutly_level, orientation=user_orientation)

        green_dirt: Dirt = Dirt(colour=Colour.green)
        green_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=green_dirt.get_id(), progressive_id=green_dirt.get_progressive_id(), colour=Colour.green)

        orange_dirt: Dirt = Dirt(colour=Colour.orange)
        orange_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=orange_dirt.get_id(), progressive_id=orange_dirt.get_progressive_id(), colour=Colour.orange)

        env, grid_size = self.__generate_empty_env(custom_grid_size=custom_grid_size)

        env.add_actor(actor=green_agent)
        env.add_actor(actor=orange_agent)
        env.add_actor(actor=white_agent)
        env.add_actor(actor=user)
        env.add_passive_body(passive_body=green_dirt)
        env.add_passive_body(passive_body=orange_dirt)

        green_agent_coord, orange_agent_coord, white_agent_coord, user_coord = self.__generate_mutually_exclusive_coordinates(amount=4, grid_size=grid_size)
        green_dirt_coord, orange_dirt_coord = self.__generate_mutually_exclusive_coordinates(amount=2, grid_size=grid_size)

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

        return env, grid_size

    def __generate_empty_env(self, custom_grid_size: bool) -> Tuple[VWEnvironment, int]:
        if custom_grid_size:
            grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)
            return VWEnvironment.generate_empty_env(config=self.__config, forced_line_dim=grid_size), grid_size
        else:
            grid_size: int = self.__default_grid_size
            return VWEnvironment.generate_empty_env(config=self.__config), grid_size

    def __generate_mutually_exclusive_coordinates(self, amount: int, grid_size: int) -> List[Coord]:
        assert amount > 1

        coords: List[Coord] = [Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))]

        for _ in range(amount - 1):
            tmp: Coord = Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            while tmp in coords:
                tmp = Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            coords.append(tmp)

        return coords


if __name__ == '__main__':
    main()
