#!/usr/bin/env python3

from unittest import main, TestCase
from typing import List
from random import choice, randint
from string import ascii_letters, digits

from vacuumworld import VacuumWorld, run
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.vwconfig_manager import VWConfigManager
from vacuumworld.gui.vwsaveload import VWSaveStateManager

import os


class TestGUIless(TestCase):
    '''
    This class tests the GUI-less mode of operation of VacuumWorld.
    '''
    def __init__(self, args) -> None:
        super(TestGUIless, self).__init__(args)

        self.__config: dict = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
        self.__min_number_of_cycles: int = 1
        self.__max_number_of_cycles: int = 100
        self.__number_of_runs: int = 10
        self.__list_of_max_cycles_per_run: List[int] = [randint(self.__min_number_of_cycles, self.__max_number_of_cycles) for _ in range(self.__number_of_runs)]

    def test_guiless(self) -> None:
        '''
        Tests the GUI-less mode of operation of VacuumWorld.
        '''
        for total_cycles in self.__list_of_max_cycles_per_run:
            try:
                env, _ = VWEnvironment.generate_random_env_for_testing(config=self.__config, custom_grid_size=True)
                test_file: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + ".json"
                manager: VWSaveStateManager = VWSaveStateManager()
                manager.save_state(env=env, filename=test_file)

                run(default_mind=VWHystereticMindSurrogate(), speed=0.999, load=test_file, total_cycles=total_cycles, gui=False, debug_enabled=False)
            except Exception as e:
                self.fail(e.args[0])
            finally:
                if os.path.exists(os.path.join(os.getcwd(), "files", test_file)):
                    os.remove(os.path.join(os.getcwd(), "files", test_file))


if __name__ == '__main__':
    main()
