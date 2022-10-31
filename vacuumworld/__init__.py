from typing import Tuple, Dict, Type, Union
from subprocess import call, DEVNULL
from sys import version_info
from traceback import print_exc
from signal import signal as handle_signal

from .config_manager import ConfigManager
from .model.actions.vwactions import VWCommunicativeAction
from .model.actor.actor_mind_surrogate import ActorMindSurrogate
from .model.actor.user_mind_surrogate import UserMindSurrogate
from .model.actor.user_difficulty import UserDifficulty
from .common.colour import Colour
from .runner.gui_runner import VWGUIRunner
from .runner.guiless_runner import VWGUIlessRunner

import os
import signal as signal_module


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
        VacuumWorld.__set_sigtstp_handler()

        self.__config_manager: ConfigManager = ConfigManager(self.CONFIG_FILE_PATH)
        self.__config: dict = self.__config_manager.load_config()

        # TODO: move this to somewhere else.
        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def run(self, default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
        self.__vw_version_check()

        minds: Dict[Colour, ActorMindSurrogate] = VacuumWorld.__process_minds(default_mind, white_mind, green_mind, orange_mind)
        minds[Colour.user] = UserMindSurrogate(difficulty_level=UserDifficulty(self.__config["default_user_mind_level"]))

        if "gui" in kwargs and type(kwargs.get("gui")) == VacuumWorld.ALLOWED_RUN_ARGS["gui"] and not kwargs.get("gui"):
            self.__run(runner_type=VWGUIlessRunner, minds=minds, **kwargs)
        else:
            self.__run(runner_type=VWGUIRunner, minds=minds, **kwargs)

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

    def __run(self, runner_type: Type[Union[VWGUIRunner, VWGUIlessRunner]], minds: Dict[Colour, ActorMindSurrogate], **kwargs) -> None:
        try:
            runner: Union[VWGUIRunner, VWGUIlessRunner] = runner_type(config=self.__config, minds=minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, **kwargs)
            runner.start()
            runner.join()
        except KeyboardInterrupt:
            print("Received a SIGINT (possibly via CTRL+C). Stopping...")

            assert "runner" in locals()

            runner.propagate_stop_signal()
            runner.join()
        except Exception:
            print_exc()
            print("Fatal error. Bye")

    @staticmethod
    def __process_minds(default_mind: ActorMindSurrogate=None, white_mind: ActorMindSurrogate=None, green_mind: ActorMindSurrogate=None, orange_mind: ActorMindSurrogate=None) -> Dict[Colour, ActorMindSurrogate]:
        assert default_mind is not None or white_mind is not None and green_mind is not None and orange_mind is not None

        if all(m is not None for m in [default_mind, white_mind, green_mind, orange_mind]):
            print("WARNING: You have specified a default mind surrogate and a mind surrogate for each of the agent colours. The default mind surrogate will be ignored.")

        # The minds are validated at a later stage.
        return {
            Colour.white: white_mind if white_mind is not None else default_mind,
            Colour.green: green_mind if green_mind is not None else default_mind,
            Colour.orange: orange_mind if orange_mind is not None else default_mind
        }

    @staticmethod
    def __set_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal_module, "SIGTSTP"):
            from signal import SIGTSTP

            handle_signal(SIGTSTP, lambda _, __: print("SIGTSTP received and ignored."))


# For back-compatibility with 4.2.5.
def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
    vw: VacuumWorld = VacuumWorld()
    vw.run(default_mind=default_mind, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, **kwargs)
