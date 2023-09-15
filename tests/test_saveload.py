#!/usr/bin/env python3

from unittest import main, TestCase
from random import choice
from string import ascii_letters, digits
from typing import Any

from vacuumworld import VacuumWorld
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.vwconfig_manager import VWConfigManager
from vacuumworld.gui.vwsaveload import VWSaveStateManager


class TestSaveLoad(TestCase):
    '''
    This class tests the save/load functionality of VacuumWorld (i.e., the `VWSaveStateManager` class).
    '''
    def __init__(self, args: Any) -> None:
        super(TestSaveLoad, self).__init__(args)

        self.__save_state_manager = VWSaveStateManager()
        self.__config: dict[str, Any] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
        self.__temp_file_deletion_after_error_message: str = "We are still deleting the temporary saved state."

    def test_save_to_file(self):
        '''
        Tests saving a `VWEnvironment` to a file.
        '''
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)
        filename: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + self.__save_state_manager.get_vw_saved_state_extension()

        try:
            self.assertTrue(self.__save_state_manager.save_state(env=env, filename=filename))
        except AssertionError as e:
            e.args += (self.__temp_file_deletion_after_error_message,)

            # We rethrow the Exception, and we delete the file in the `finally` block.
            raise e
        finally:
            self.__save_state_manager.remove_saved_state(filename=filename)

    def test_load_from_file(self):
        '''
        Tests loading a `VWEnvironment` from a file.
        '''
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)
        filename: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + self.__save_state_manager.get_vw_saved_state_extension()

        try:
            self.assertTrue(self.__save_state_manager.save_state(env=env, filename=filename))

            loaded_grid: dict[str, Any] = self.__save_state_manager.load_state(filename=filename)
            loaded_env: VWEnvironment = VWEnvironment.from_json(data=loaded_grid, config=self.__config)

            self.assertTrue(TestSaveLoad.__env_match(env, loaded_env))
        except AssertionError as e:
            e.args += (self.__temp_file_deletion_after_error_message,)

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

        for coord in [VWCoord(x=x, y=y) for x in range(env1.get_ambient().get_grid_dim()) for y in range(env1.get_ambient().get_grid_dim())]:
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
            return loc1.get_actor_appearance().or_else_raise().equals_except_ids(loc2.get_actor_appearance().or_else_raise()) and loc1.get_dirt_appearance().or_else_raise().equals_except_ids(loc2.get_dirt_appearance().or_else_raise())
        elif loc1.has_actor():
            return loc1.get_actor_appearance().or_else_raise().equals_except_ids(loc2.get_actor_appearance().or_else_raise())
        elif loc1.has_dirt():
            return loc1.get_dirt_appearance().or_else_raise().equals_except_ids(loc2.get_dirt_appearance().or_else_raise())

        return True


if __name__ == '__main__':
    main()
