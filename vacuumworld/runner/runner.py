from typing import Dict, Union, Type
from traceback import print_exc
from multiprocessing import Process, Event
from multiprocessing.synchronize import Event as EventType
from inspect import getsourcefile
from signal import signal as handle_signal

from ..common.colour import Colour
from ..model.actions.vwactions import VWAction, VWCommunicativeAction
from ..model.actions.effort import ActionEffort
from ..model.actor.actor_mind_surrogate import ActorMindSurrogate
from ..model.actor.actor_behaviour_debugger import ActorBehaviourDebugger
from ..model.environment.vwenvironment import VWEnvironment
from ..gui.saveload import SaveStateManager

import signal as signal_module


class VWRunner(Process):
    def __init__(self, config: dict, minds: Dict[Colour, ActorMindSurrogate], allowed_args: Dict[str, Type], **kwargs) -> None:
        super(VWRunner, self).__init__()

        self.__config: dict = config
        self.__minds: Dict[Colour, ActorMindSurrogate] = minds
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
        self.__save_state_manager: SaveStateManager = SaveStateManager()
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
        return self.__config

    def get_minds(self) -> Dict[Colour, ActorMindSurrogate]:
        return self.__minds

    def get_arg(self, arg: str) -> Union[bool, int, float, str, Dict[str, int]]:
        return self.__args[arg]

    def get_save_state_manager(self) -> SaveStateManager:
        return self.__save_state_manager

    def can_loop(self) -> bool:
        return not self.__forceful_stop

    def must_stop_now(self) -> bool:
        return self.__exit.is_set()

    def propagate_stop_signal(self) -> None:
        self.__exit.set()

    def kill(self) -> None:
        self.__forceful_stop = True

    def clean_exit(self) -> None:
        print_exc()

        self.kill()

    def load_env(self) -> VWEnvironment:
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
        raise NotImplementedError()

    def __validate_minds(self) -> None:
        if not all(isinstance(self.__minds[colour], self.__allowed_args[str(colour) + "_mind"]) for colour in Colour if colour != Colour.user):
            raise ValueError("One or more mind surrogates are not of the allowed type.")

        for colour, mind in self.__minds.items():
            ActorMindSurrogate.validate(mind=mind, colour=colour)

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
        elif not all(effort_name in ActionEffort.EFFORTS for effort_name in self.__args["efforts"]):
            raise ValueError("Invalid effort name: it should be one of {}, but it is `{}`".format([k for k in ActionEffort.EFFORTS], [e for e in self.__args["efforts"] if e not in ActionEffort.EFFORTS][0]))

    def __validate_debug_enabled_flag(self) -> None:
        if not isinstance(self.__args["debug_enabled"], self.__allowed_args["debug_enabled"]):
            raise TypeError("Argument `debug_enabled` must be a boolean.")

    def __override_default_config(self) -> None:
        # The content of `self.__minds` has already been validated in `__validate_minds()`.
        # The content of `self.__args` has already been validated in `__validate_optional_args()`.

        self.__config["white_mind_filename"] = getsourcefile(self.__minds[Colour.white].__class__)
        self.__config["orange_mind_filename"] = getsourcefile(self.__minds[Colour.orange].__class__)
        self.__config["green_mind_filename"] = getsourcefile(self.__minds[Colour.green].__class__)
        self.__config["user_mind_filename"] = getsourcefile(self.__minds[Colour.user].__class__)
        self.__config["skip"] |= self.__args["skip"]
        self.__config["play"] |= self.__args["play"]
        self.__config["time_step_modifier"] = 1 - self.__args["speed"]
        self.__config["file_to_load"] = self.__args["load"]
        self.__config["scale"] = self.__args["scale"]
        self.__config["x_scale"] = self.__args["scale"]
        self.__config["y_scale"] = self.__args["scale"]
        self.__config["tooltips"] &= self.__args["tooltips"]
        self.__config["total_cycles"] = self.__args["total_cycles"]

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
                ActionEffort.override_default_effort_for_action(action_name=k.__name__, new_effort=v)

                print("The effort of {} is now {}.".format(k.__name__, ActionEffort.EFFORTS[k.__name__]))
            elif type(k) == str and type(v) == int:
                ActionEffort.override_default_effort_for_action(action_name=k, new_effort=v)

                print("The effort of {} is now {}.".format(k, ActionEffort.EFFORTS[k]))

        print()

    def __manage_sender_id_spoofing_rule(self) -> None:
        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def __manage_debug_flag(self) -> None:
        assert "debug_enabled" in self.__args and isinstance(self.__args["debug_enabled"], bool)

        ActorBehaviourDebugger.DEBUG_ENABLED = self.__args["debug_enabled"]

    @staticmethod
    def __set_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal_module, "SIGTSTP"):
            from signal import SIGTSTP

            handle_signal(SIGTSTP, lambda _, __: print("SIGTSTP received and ignored."))
