from typing import Dict, Union, Type, List
from traceback import print_exc
from multiprocessing import Process, Event
from multiprocessing.synchronize import Event as EventType
from inspect import getsourcefile
from signal import signal as handle_signal

from ..common.vwcolour import VWColour
from ..model.actions.vwactions import VWAction, VWCommunicativeAction
from ..model.actions.vweffort import VWActionEffort
from ..model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from ..model.actor.vwactor_behaviour_debugger import VWActorBehaviourDebugger
from ..model.environment.vwenvironment import VWEnvironment
from ..gui.vwsaveload import VWSaveStateManager

import signal as signal_module


class VWRunner(Process):
    '''
    This abstract class is the base for all the VacuumWorld runners. It contains all the common methods and attributes.

    All the runners must implement the `run()` method.

    All the arguments passed to `VacuumWorld.run()`are stored and validated here, together with their default values.
    '''
    def __init__(self, config: dict, minds: Dict[VWColour, VWActorMindSurrogate], allowed_args: Dict[str, Type], **kwargs) -> None:
        super(VWRunner, self).__init__()

        self.__config: dict = config
        self.__minds: Dict[VWColour, VWActorMindSurrogate] = minds
        self.__allowed_args: Dict[str, Type] = allowed_args
        self.__args: Dict[str, Union[bool, int, float, str, Dict[str, int]]] = {
            "gui": kwargs.get("gui", True),
            "skip": kwargs.get("skip", False),
            "play": kwargs.get("play", False),
            "load": kwargs.get("load", ""),
            "speed": kwargs.get("speed", 0.0),
            "scale": kwargs.get("scale", 1.0),
            "tooltips": kwargs.get("tooltips", True),
            "total_cycles": kwargs.get("total_cycles", 0),
            "efforts": kwargs.get("efforts", {}),
            "debug_enabled": kwargs.get("debug_enabled", True)
        }
        self.__save_state_manager: VWSaveStateManager = VWSaveStateManager()
        self.__forceful_stop: bool = False
        self.__exit: EventType = Event()

        self.__validate_minds()
        self.__validate_optional_args()
        self.__override_default_config()
        self.__scale_config_parameters()
        self.__assign_efforts_to_actions()
        self.__manage_sender_id_spoofing_rule()
        self.__manage_debug_flag()

        VWRunner.__set_sigtstp_handler()

    def get_config(self) -> dict:
        '''
        Returns the configuration `dict`.
        '''
        return self.__config

    def get_minds(self) -> Dict[VWColour, VWActorMindSurrogate]:
        '''
        Returns a `Dict[Colour, ActorMindSurrogate]` mapping each `VWColour` to a `VWActorMindSurrogate` that will be given to each `VWActor` exhibiting that particular `VWColour`.
        '''
        return self.__minds

    def get_arg(self, arg: str) -> Union[bool, int, float, str, Dict[str, int]]:
        '''
        Returns the value of the argument `arg` as a `Union[bool, int, float, Dict[str, int]]`.
        '''
        return self.__args[arg]

    def get_save_state_manager(self) -> VWSaveStateManager:
        '''
        Returns the `VWSaveStateManager` used by this `VWRunner`.
        '''
        return self.__save_state_manager

    def can_loop(self) -> bool:
        '''
        Returns whether or not this `VWRunner` can keep looping.

        If a `VWRunner` cannot loop, it means that some internal error has been raised, and the `VWRunner` must stop as a consequence.
        '''
        return not self.__forceful_stop

    def must_stop_now(self) -> bool:
        '''
        Returns whether or not this `VWRunner` must stop now.

        If a `VWRunner` must stop now, it means that the user (or the Kernel) has requested to stop the execution of the `VWRunner` with something like a `KeyboardInterrupt`.
        '''
        return self.__exit.is_set()

    def propagate_stop_signal(self) -> None:
        '''
        Sets the `Event` signalling an external interrupt to `True`, so that this `VWRunner` can stop.
        '''
        self.__exit.set()

    def kill(self) -> None:
        '''
        Sets the `bool` signalling an internal interrupt to `True`, so that this `VWRunner` can stop.
        '''
        self.__forceful_stop = True

    def clean_exit(self) -> None:
        '''
        Displays an internal error message and sets the `bool` signalling an internal interrupt to `True`, so that this `VWRunner` can stop.
        '''
        print_exc()

        self.kill()

    def load_env(self) -> VWEnvironment:
        '''
        Attempts to load and return a `VWEnvironment` from the file specified by `config[\"file_to_load\"]` (which was set according to the `load` argument).

        If an error occurs, an empty `VWEnvironment` with a default grid size is generated and returned instead.
        '''
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

    def run(self) -> None:
        '''
        This abstract method must be implemented by all the `VWRunner` subclasses.
        '''
        raise NotImplementedError()

    def __validate_minds(self) -> None:
        if not all(isinstance(self.__minds[colour], self.__allowed_args[str(colour) + "_mind"]) for colour in VWColour if colour != VWColour.user):
            raise TypeError("One or more mind surrogates are not of the allowed type.")

        for colour, mind in self.__minds.items():
            VWActorMindSurrogate.validate(mind=mind, colour=colour, surrogate_mind_type=self.__allowed_args[str(colour) + "_mind"])

    def __validate_optional_args(self) -> None:
        self.__validate_play_load()
        self.__validate_skip()
        self.__validate_speed()
        self.__validate_scale()
        self.__validate_tooltips()
        self.__validate_total_cycles()
        self.__validate_efforts()
        self.__validate_debug_enabled_flag()

    def __validate_play_load(self) -> None:
        if not isinstance(self.__args["play"], self.__allowed_args["play"]):
            raise TypeError("Argument `play` must be a boolean.")

        if not isinstance(self.__args["load"], self.__allowed_args["load"]):
            raise TypeError("Argument `load` must be a string.")

        if self.__args["play"] and not self.__args["load"]:
            raise ValueError("Argument `load` must be specified if argument `play` is `True`")

    def __validate_skip(self) -> None:
        if not isinstance(self.__args["skip"], self.__allowed_args["skip"]):
            raise TypeError("Argument `skip` must be a boolean.")

    def __validate_speed(self) -> None:
        if not isinstance(self.__args["speed"], self.__allowed_args["speed"]):
            raise TypeError("Argument `speed` must be a float.")

        if self.__args["speed"] < 0 or self.__args["speed"] >= 1:
            raise ValueError("Argument \"speed\" must be >=0 and < 1.")

    def __validate_scale(self) -> None:
        if not isinstance(self.__args["scale"], self.__allowed_args["scale"]):
            raise TypeError("Argument `scale` must be a float.")

        # A 0 value is equivalent to omitting the argument from `vacuumworld.run()`.
        if self.__args["scale"] < 0 or self.__args["scale"] > 2.5:
            raise ValueError("Argument \"scale\" must be >= 0 and <= 2.5.")

    def __validate_tooltips(self) -> None:
        if not isinstance(self.__args["tooltips"], self.__allowed_args["tooltips"]):
            raise TypeError("Argument `tooltips` must be a boolean.")

    def __validate_total_cycles(self) -> None:
        if not isinstance(self.__args["total_cycles"], self.__allowed_args["total_cycles"]):
            raise TypeError("Argument `total_cycles` must be an integer.")

        # A 0 value means an infinite number of cycles.
        if self.__args["total_cycles"] < 0:
            raise ValueError("Argument \"total_cycles\" must be >= 0.")

    def __validate_efforts(self) -> None:
        if not isinstance(self.__args["efforts"], dict):
            raise TypeError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but it is `{}`".format(type(self.__args["efforts"])))
        elif not all(isinstance(key, str) for key in self.__args["efforts"].keys()):
            raise TypeError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but there is at least a key that is not a `str`")
        elif not all(isinstance(value, int) for value in self.__args["efforts"].values()):
            raise TypeError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but there is at least a value that is not an `int`")
        elif not all(effort_name in VWActionEffort.EFFORTS for effort_name in self.__args["efforts"]):
            raise ValueError("Invalid effort name: it should be one of {}, but it is `{}`".format([k for k in VWActionEffort.EFFORTS], [e for e in self.__args["efforts"] if e not in VWActionEffort.EFFORTS][0]))

    def __validate_debug_enabled_flag(self) -> None:
        if not isinstance(self.__args["debug_enabled"], self.__allowed_args["debug_enabled"]):
            raise TypeError("Argument `debug_enabled` must be a boolean.")

    def __override_default_config(self) -> None:
        # The content of `self.__minds` has already been validated in `__validate_minds()`.
        # The content of `self.__args` has already been validated in `__validate_optional_args()`.

        self.__config["white_mind_filename"] = getsourcefile(self.__minds[VWColour.white].__class__)
        self.__config["orange_mind_filename"] = getsourcefile(self.__minds[VWColour.orange].__class__)
        self.__config["green_mind_filename"] = getsourcefile(self.__minds[VWColour.green].__class__)
        self.__config["user_mind_filename"] = getsourcefile(self.__minds[VWColour.user].__class__)
        self.__config["skip"] |= self.__args["skip"]
        self.__config["play"] |= self.__args["play"]
        self.__config["time_step_modifier"] = 1 - self.__args["speed"]
        self.__config["file_to_load"] = self.__args["load"]
        self.__config["scale"] = self.__args["scale"]
        self.__config["x_scale"] = self.__args["scale"]
        self.__config["y_scale"] = self.__args["scale"]
        self.__config["tooltips"] &= self.__args["tooltips"]
        self.__config["total_cycles"] = self.__args["total_cycles"]
        self.__config["debug"] &= self.__args["debug_enabled"]

    def __scale_config_parameters(self) -> None:
        self.__config["grid_size"] *= self.__config["scale"]
        self.__config["button_size"] *= self.__config["scale"]
        self.__config["location_size"] *= self.__config["scale"]
        self.__config["root_font"][1] = int(self.__config["root_font"][1] * self.__config["scale"])
        self.__config["time_step"] = self.__config["time_step"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

    def __load_grid_data_from_file(self, filename: str) -> dict:
        data: dict = self.__save_state_manager.load_state(filename=filename, no_gui=True)

        if data:
            print("The saved grid was successfully loaded.")

            return data
        else:
            print("The state was not loaded.")

            return {}

    def __assign_efforts_to_actions(self) -> None:
        # The content of `self.__args` has already been validated in `__validate_optional_args()`.
        for k, v in self.__args["efforts"].items():
            if type(k) == type and issubclass(k, VWAction) and type(v) == int:
                VWActionEffort.override_default_effort_for_action(action_name=k.__name__, new_effort=v)

                print("The effort of {} is now {}.".format(k.__name__, VWActionEffort.EFFORTS[k.__name__]))
            elif type(k) == str and type(v) == int:
                VWActionEffort.override_default_effort_for_action(action_name=k, new_effort=v)

                print("The effort of {} is now {}.".format(k, VWActionEffort.EFFORTS[k]))

        print()

    def __manage_sender_id_spoofing_rule(self) -> None:
        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def __manage_debug_flag(self) -> None:
        VWActorBehaviourDebugger.DEBUG_ENABLED: bool = self.__config["debug"]

        if self.__config["debug_test"]:
            VWActorBehaviourDebugger.PRIMES: List[int] = self.__config["debug_primes_test"]
        else:
            VWActorBehaviourDebugger.PRIMES: List[int] = self.__config["debug_primes"]

    @staticmethod
    def __set_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal_module, "SIGTSTP"):
            from signal import SIGTSTP

            handle_signal(SIGTSTP, lambda _, __: print("SIGTSTP received and ignored."))
