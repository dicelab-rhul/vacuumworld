#!/usr/bin/env python3

from unittest import main, TestCase
from typing import List
from random import choice
from string import ascii_letters, digits

from vacuumworld import run
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.config_manager import ConfigManager
from vacuumworld.gui.saveload import SaveStateManager

import os


class TestGUIless(TestCase):
    def __init__(self, args) -> None:
        super(TestGUIless, self).__init__(args)

        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vacuumworld", "config.json")
        self.__config: dict = ConfigManager(config_file_path=self.__config_file_path).load_config()
        self.__list_of_max_cycles_per_run: List[int] = [1, 5, 10, 20, 50, 100]

    def test_guiless(self) -> None:
        for total_cycles in self.__list_of_max_cycles_per_run:
            try:
                env, _ = VWEnvironment.generate_random_env_for_testing(config=self.__config, custom_grid_size=True)
                test_file: str = "".join([choice(ascii_letters + digits) for _ in range(10)]) + ".json"
                manager: SaveStateManager = SaveStateManager()
                manager.save_state(env=env, filename=test_file)

                run(default_mind=VWHystereticMindSurrogate(), speed=0.999, load=test_file, total_cycles=total_cycles, gui=False)
            except Exception as e:
                self.fail(e.args[0])
            finally:
                os.remove(os.path.join(os.getcwd(), "files", test_file))


if __name__ == '__main__':
    main()
