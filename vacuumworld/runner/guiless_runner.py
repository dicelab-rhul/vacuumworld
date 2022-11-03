from typing import Dict, Type
from time import sleep

from .runner import VWRunner
from ..common.colour import Colour
from ..model.actor.actor_mind_surrogate import ActorMindSurrogate
from ..model.environment.vwenvironment import VWEnvironment


class VWGUIlessRunner(VWRunner):
    def __init__(self, config: dict, minds: Dict[Colour, ActorMindSurrogate], allowed_args: Dict[str, Type], **kwargs) -> None:
        super(VWGUIlessRunner, self).__init__(config=config, minds=minds, allowed_args=allowed_args, **kwargs)

        self.__validate_load()

    def run(self) -> None:
        try:
            env: VWEnvironment = self.load_env()

            print("Initial environment:\n\n{}\n".format(env))

            self.__loop(env=env)
        except KeyboardInterrupt:
            return
        except Exception:
            self.clean_exit()

    def __loop(self, env: VWEnvironment) -> None:
        while not self.must_stop_now():  # This is for external interrupts (e.g., `KeyboardInterrupt`).
            if self.can_loop():  # This is for internal interrupts (e.g., any `Exception`).
                self.__do_loop(env=env)
            else:
                break

    def __do_loop(self, env: VWEnvironment) -> None:
        if env.get_current_cycle_number() >= 0:
            print("------------ Cycle {} ------------ ".format(env.get_current_cycle_number()))

        env.evolve()

        if env.get_current_cycle_number() >= 0:
            print("\nEnvironment at the end of cycle {}:\n\n{}\n".format(env.get_current_cycle_number(), env))

        sleep(int(self.get_config()["time_step"]))

        if self.get_config()["total_cycles"] > 0 and env.get_current_cycle_number() == self.get_config()["total_cycles"]:
            print("INFO: end of cycles.")

            self.kill()

    def __validate_load(self) -> None:
        if not self.get_config()["file_to_load"]:
            raise ValueError("VacuumWorld cannot run GUI-less if no savestate file is provided.")