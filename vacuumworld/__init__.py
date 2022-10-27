from signal import signal, SIG_IGN
from typing import Tuple, Dict, Type, Any
from subprocess import call, DEVNULL
from sys import version_info

from .config_manager import ConfigManager
from .model.actions.vwactions import VWAction
from .model.actions.vwactions import VWCommunicativeAction
from .model.actions.effort import ActionEffort
from .model.actor.actor_mind_surrogate import ActorMindSurrogate
from .model.actor.user_mind_surrogate import UserMindSurrogate
from .model.actor.user_difficulty import UserDifficulty
from .common.colour import Colour
from .gui.gui import VWGUI
from .guiless import VWGuilessRunner

import os


class VacuumWorld():
    CONFIG_FILE_NAME: str = "config.json"
    CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)
    MIN_PYTHON_VERSION: Tuple[int, int] = (3, 8)
    ALLOWED_RUN_ARGS: Dict[str, Type] = {
        "default_mind": ActorMindSurrogate,
        "green_mind": ActorMindSurrogate,
        "orange_mind": ActorMindSurrogate,
        "white_mind": ActorMindSurrogate,
        "gui": bool,
        "skip": bool,
        "play": bool,
        "load": str,
        "speed": float,
        "scale": float,
        "tooltips": bool,
        "efforts": Dict[str, int],
        "total_cycles": int
    }

    def __init__(self) -> None:
        VacuumWorld.__python_version_check()
        VacuumWorld.__setup_sigtstp_handler()

        self.__config_manager: ConfigManager = ConfigManager(self.CONFIG_FILE_PATH)
        self.__config: dict = self.__config_manager.load_config()

        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def run(self, default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
        self.__vw_version_check()

        VacuumWorld.__check_kwargs_names_and_types(**kwargs)
        VacuumWorld.__assign_efforts_to_actions(**kwargs)

        white_mind, green_mind, orange_mind = VacuumWorld.__process_minds(default_mind, white_mind, green_mind, orange_mind)
        user_mind: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty(self.__config["default_user_mind_level"]))

        if "gui" in kwargs and not kwargs.get("gui"):
            self.__run_guiless(white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)
        else:
            self.__run_with_gui(white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)

    @staticmethod
    def __check_kwargs_names_and_types(**kwargs) -> None:
        for arg in kwargs:
            if arg not in VacuumWorld.ALLOWED_RUN_ARGS:
                raise ValueError("Invalid argument for `run()`: {}".format(arg))

            # This needs to change in case we add another argument that is a `Dict`.
            if VacuumWorld.ALLOWED_RUN_ARGS.get(arg) == Dict[str, int]:
                VacuumWorld.__validate_efforts(kwargs.get(arg))
            elif not isinstance(kwargs.get(arg), VacuumWorld.ALLOWED_RUN_ARGS.get(arg)):
                raise ValueError("Invalid type for argument `{}`: it should be `{}`, but it is `{}`".format(arg, VacuumWorld.ALLOWED_RUN_ARGS[arg], type((kwargs.get(arg)))))

    @staticmethod
    def __validate_efforts(efforts: Any) -> None:
        if not isinstance(efforts, dict):
            raise ValueError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but it is `{}`".format(type(efforts)))
        elif not all(isinstance(key, str) for key in efforts.keys()):
            raise ValueError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but there is at least a key that is not a `str`")
        elif not all(isinstance(value, int) for value in efforts.values()):
            raise ValueError("Invalid type for argument `efforts`: it should be `Dict[str, int]`, but there is at least a value that is not an `int`")
        elif not all(effort_name in ActionEffort.EFFORTS for effort_name in efforts):
            raise ValueError("Invalid effort name: it should be one of {}, but it is `{}`".format([k for k in ActionEffort.EFFORTS], [e for e in efforts if e not in ActionEffort.EFFORTS][0]))

    @staticmethod
    def __python_version_check() -> None:
        if version_info.major < VacuumWorld.MIN_PYTHON_VERSION[0] or version_info.minor < VacuumWorld.MIN_PYTHON_VERSION[1]:
            print("VacuumWorld requires Python {}.{} or later. Please install Python {}.{} or later and try again.".format(VacuumWorld.MIN_PYTHON_VERSION[0], VacuumWorld.MIN_PYTHON_VERSION[1], VacuumWorld.MIN_PYTHON_VERSION[0], VacuumWorld.MIN_PYTHON_VERSION[1]))

            exit(1)

    def __vw_version_check(self) -> None:
        try:
            version_number: str = self.__config["version_number"]

            print("VacuumWorld version: {}.\n".format(version_number))

            call(["wget", "https://raw.githubusercontent.com/dicelab-rhul/vacuumworld/main/vacuumworld/{}".format(VacuumWorld.CONFIG_FILE_NAME)], stdout=DEVNULL, stderr=DEVNULL)

            remote_config: dict = ConfigManager(config_file_path=VacuumWorld.CONFIG_FILE_NAME).load_config()
            latest_version_number: str = remote_config["version_number"]

            if version_number != latest_version_number:
                print("WARNING: Your version of VacuumWorld is outdated. The latest version is {}.".format(latest_version_number))
                print("Please update VacuumWorld by running `./update_vw.sh` from a terminal, after navigating to the cloned directory.\n")
            else:
                print("Your version of VacuumWorld is up-to-date.\n")
        finally:
            if os.path.exists(VacuumWorld.CONFIG_FILE_NAME):
                os.remove(VacuumWorld.CONFIG_FILE_NAME)

    @staticmethod
    def __setup_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal, "SIGTSTP"):
            from signal import SIGTSTP

            signal(SIGTSTP, SIG_IGN)

    @staticmethod
    def __assign_efforts_to_actions(**kwargs) -> None:
        if "efforts" in kwargs and type(kwargs["efforts"]) == dict:
            for k, v in kwargs["efforts"].items():
                if type(k) == type and issubclass(k, VWAction) and type(v) == int:
                    ActionEffort.override_default_effort_for_action(action_name=k.__name__, new_effort=v)

                    print("The effort of {} is now {}.".format(k.__name__, ActionEffort.EFFORTS[k.__name__]))
                elif type(k) == str and type(v) == int:
                    ActionEffort.override_default_effort_for_action(action_name=k, new_effort=v)

                    print("The effort of {} is now {}.".format(k, ActionEffort.EFFORTS[k]))

            print()

    def __run_guiless(self, white_mind: ActorMindSurrogate, green_mind: ActorMindSurrogate, orange_mind: ActorMindSurrogate, user_mind: UserMindSurrogate, **kwargs) -> None:
        if "load" not in kwargs or not kwargs.get("load"):
            print("VacuumWorld cannot run GUI-less if no savestate file is provided.")
        else:
            print("RunningGUI-less...")

            minds: Dict[Colour, ActorMindSurrogate] = {Colour.white: white_mind, Colour.green: green_mind, Colour.orange: orange_mind, Colour.user: user_mind}
            speed: float = kwargs.get("speed") if "speed" in kwargs else 0.0
            load: str = kwargs.get("load") if "load" in kwargs else None
            total_cycles: int = kwargs.get("total_cycles") if "total_cycles" in kwargs else 0

            vw_runner: VWGuilessRunner = VWGuilessRunner(config=self.__config, minds=minds, speed=speed, load=load, total_cycles=total_cycles)
            vw_runner.start()

    def __run_with_gui(self, white_mind: ActorMindSurrogate, green_mind: ActorMindSurrogate, orange_mind: ActorMindSurrogate, user_mind: UserMindSurrogate, **kwargs) -> None:
        vwgui: VWGUI = VWGUI(config=self.__config)

        try:
            vwgui.init_gui_conf(minds={Colour.white: white_mind, Colour.green: green_mind, Colour.orange: orange_mind, Colour.user: user_mind}, **kwargs)
            vwgui.start()
            vwgui.join()
        except KeyboardInterrupt:
            print("Received a SIGINT (possibly via CTRL+C). Stopping...")
            vwgui.propagate_stop_signal()
            vwgui.join()
        except Exception as e:
            print("Fatal error: {}. Bye".format(e))

    @staticmethod
    def __process_minds(default_mind: ActorMindSurrogate=None, white_mind: ActorMindSurrogate=None, green_mind: ActorMindSurrogate=None, orange_mind: ActorMindSurrogate=None) -> Tuple[ActorMindSurrogate, ActorMindSurrogate, ActorMindSurrogate]:
        assert default_mind is not None or white_mind is not None and green_mind is not None and orange_mind is not None

        if all(m is not None for m in [default_mind, white_mind, green_mind, orange_mind]):
            print("WARNING: You have specified a default mind surrogate and a mind surrogate for each of the agent colours. The default mind surrogate will be ignored.")

        minds: Dict[Colour, ActorMindSurrogate] = {
            Colour.green: white_mind if white_mind is not None else default_mind,
            Colour.orange: green_mind if green_mind is not None else default_mind,
            Colour.white: orange_mind if orange_mind is not None else default_mind
        }

        if not all(isinstance(minds[colour], VacuumWorld.ALLOWED_RUN_ARGS[str(colour) + "_mind"]) for colour in Colour if colour != Colour.user):
            raise ValueError("One or more mind surrogates are not of the allowed type.")

        for colour, mind in minds.items():
            ActorMindSurrogate.validate(mind=mind, colour=colour)

        return minds


# For back-compatibility with 4.2.5.
def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
    vw: VacuumWorld = VacuumWorld()
    vw.run(default_mind=default_mind, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, **kwargs)
