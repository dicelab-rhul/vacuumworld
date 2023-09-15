from typing import Dict, Type, Any
from time import sleep

from .vwrunner import VWRunner
from ..common.vwcolour import VWColour
from ..model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from ..model.environment.vwenvironment import VWEnvironment


class VWGUIlessRunner(VWRunner):
    '''
    This class is responsible for running VacuumWorld without a GUI.
    '''
    def __init__(self, config: dict[str, Any], minds: Dict[VWColour, VWActorMindSurrogate], allowed_args: Dict[str, Type[Any]], **kwargs: Any) -> None:
        super(VWGUIlessRunner, self).__init__(config=config, minds=minds, allowed_args=allowed_args, **kwargs)

        self.__validate_load()

    def run(self) -> None:
        '''
        Runs the simulation.

        If a `KeyboardInterrupt` is raised, the simulation is stopped.

        If any other `Exception` is raised, the simulation is stopped, and the error message is passed to the user.
        '''
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
            raise ValueError("VacuumWorld cannot run GUI-less if no savestate file is provided via the `load` argument.")
