from typing import Dict
from inspect import getsourcefile
from time import sleep
from traceback import print_exc

from .common.colour import Colour
from .model.actor.actor_mind_surrogate import ActorMindSurrogate
from .model.environment.vwenvironment import VWEnvironment
from .gui.saveload import SaveStateManager



class VWGuilessRunner():
    def __init__(self, config: dict, minds: Dict[Colour, ActorMindSurrogate], load: str=None, speed: float=0.0) -> None:
        assert config
        assert minds
        assert load
        assert speed >= 0 and speed < 1

        self.__config: dict = config
        self.__minds: Dict[Colour, ActorMindSurrogate] = minds
        self.__config["white_mind_filename"] = getsourcefile(self.__minds[Colour.white].__class__)
        self.__config["orange_mind_filename"] = getsourcefile(self.__minds[Colour.orange].__class__)
        self.__config["green_mind_filename"] = getsourcefile(self.__minds[Colour.green].__class__)
        self.__config["user_mind_filename"] = getsourcefile(self.__minds[Colour.user].__class__)
        self.__config["file_to_load"] = load
        self.__config["time_step_modifier"] = 1 - speed
        self.__config["time_step"] = self.__config["time_step"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]
        self.__save_state_manager: SaveStateManager = SaveStateManager()

    def start(self) -> None:
        self.run()

    def run(self) -> None:
        try:
            env: VWEnvironment = self.__load_env()

            print("Initial environment:\n\n{}\n".format(env))

            while True:        
                print("------------ Cycle {} ------------ ".format(env.get_current_cycle_number()))
    
                env.evolve()

                print("\nEnvironment at the end of cycle {}:\n\n{}\n".format(env.get_current_cycle_number() - 1, env))

                sleep(int(self.__config["time_step"]))
        except KeyboardInterrupt:
            print("Received a SIGINT (possibly via CTRL+C). Stopping...")
        except Exception:
            print("INFO: SIMULATION ERROR!")
            print_exc()
            print("INFO: stopping...")

    def __load_env(self) -> VWEnvironment:
        try:
            data: dict = {}

            if self.__config["file_to_load"]:
                data = self.__load_grid_data_from_file(filename=self.__config["file_to_load"])

            return VWEnvironment.from_json(data=data, config=self.__config)
        except Exception:
            if self.__config["file_to_load"] not in (None, ""):
                print("Something went wrong. Could not load any grid from {}".format(self.__config["file_to_load"]))
            else:
                print("Something went wrong. Could not load any grid.")

            return VWEnvironment.generate_empty_env(config=self.__config)

    def __load_grid_data_from_file(self, filename: str) -> dict:
        data: dict = self.__save_state_manager.load_state(filename=filename, no_gui=True)

        if data:
            print("The saved grid was successfully loaded.")
            return data
        else:
            print("The state was not loaded.")
            return {}
