from typing import Tuple, Dict, Type, List
from sys import version_info
from traceback import print_exc
from signal import signal as handle_signal
from requests import get, Response
from time import sleep
from screeninfo import get_monitors

from .vwconfig_manager import VWConfigManager
from .model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from .model.actor.mind.surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from .common.vwuser_difficulty import VWUserDifficulty
from .common.vwcolour import VWColour
from .runner.vwrunner import VWRunner
from .runner.vwgui_runner import VWGUIRunner
from .runner.vwguiless_runner import VWGUIlessRunner

import os
import signal as signal_module


class VacuumWorld():
    CONFIG_FILE_NAME: str = "config.json"
    CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)
    MIN_PYTHON_VERSION: Tuple[int, int] = (3, 8)
    ALLOWED_RUN_ARGS: Dict[str, Type] = {
        "default_mind": VWActorMindSurrogate,
        "green_mind": VWActorMindSurrogate,
        "orange_mind": VWActorMindSurrogate,
        "white_mind": VWActorMindSurrogate,
        "gui": bool,
        "skip": bool,
        "play": bool,
        "load": str,
        "speed": float,
        "scale": float,
        "tooltips": bool,
        "efforts": Dict[str, int],
        "total_cycles": int,
        "debug_enabled": bool
    }

    def __init__(self) -> None:
        VacuumWorld.__python_version_check()
        VacuumWorld.__set_sigtstp_handler()

        self.__config: dict = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)

        self.__vw_version_check()

    def run(self, default_mind: VWActorMindSurrogate=None, white_mind: VWActorMindSurrogate=None, green_mind: VWActorMindSurrogate=None, orange_mind: VWActorMindSurrogate=None, **kwargs) -> None:
        minds: Dict[VWColour, VWActorMindSurrogate] = VacuumWorld.__process_minds(default_mind=default_mind, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind)
        minds[VWColour.user] = VWUserMindSurrogate(difficulty_level=VWUserDifficulty(self.__config["default_user_mind_level"]))

        if "gui" in kwargs and type(kwargs.get("gui")) == VacuumWorld.ALLOWED_RUN_ARGS["gui"] and not kwargs.get("gui"):
            self.__run(runner_type=VWGUIlessRunner, minds=minds, **kwargs)
        elif VacuumWorld.__display_available():
            self.__run(runner_type=VWGUIRunner, minds=minds, **kwargs)
        else:
            print("WARNING: no display available. Falling back to GUI-less mode.\n")

            sleep(3)

            self.__run(runner_type=VWGUIlessRunner, minds=minds, **kwargs)

    @staticmethod
    def __display_available() -> bool:
        try:
            return len(get_monitors()) > 0
        except Exception:
            return False

    @staticmethod
    def __python_version_check() -> None:
        if VacuumWorld.__unsupported_python_version():
            print("VacuumWorld requires Python {}.{} or later. Please install Python {}.{} or later and try again.".format(VacuumWorld.MIN_PYTHON_VERSION[0], VacuumWorld.MIN_PYTHON_VERSION[1], VacuumWorld.MIN_PYTHON_VERSION[0], VacuumWorld.MIN_PYTHON_VERSION[1]))

            exit(1)
        else:
            print("Python version: {}.{}.{}. Good!".format(version_info.major, version_info.minor, version_info.micro))

    @staticmethod
    def __unsupported_python_version() -> bool:
        if version_info.major < VacuumWorld.MIN_PYTHON_VERSION[0]:
            return True
        elif version_info.major == VacuumWorld.MIN_PYTHON_VERSION[0] and version_info.minor < VacuumWorld.MIN_PYTHON_VERSION[1]:
            return True
        else:
            return False

    def __vw_version_check(self) -> None:
        version_number: str = self.__config["version_number"]
        remote_version_number: str = VacuumWorld.__get_remote_version_number()

        VacuumWorld.__compare_version_numbers_and_print_message(version_number, remote_version_number)

    @staticmethod
    def __download_remote_config() -> str:
        try:
            remote_config_url: str = "https://raw.githubusercontent.com/dicelab-rhul/vacuumworld/main/vacuumworld/{}".format(VacuumWorld.CONFIG_FILE_NAME)
            remote_config_downloaded_name: str = "remote_{}".format(VacuumWorld.CONFIG_FILE_NAME)

            response: Response = get(remote_config_url, allow_redirects=True, timeout=5)

            if response and response.status_code == 200:
                with open(remote_config_downloaded_name, "w") as remote_config_file:
                    remote_config_file.write(response.text)

                return remote_config_downloaded_name
            else:
                raise IOError("Could not download remote config file.")
        except Exception:
            return ""

    @staticmethod
    def __get_remote_version_number() -> str:
        remote_config_path: str = VacuumWorld.__download_remote_config()

        if not remote_config_path:
            return ""

        try:
            remote_config: dict = VWConfigManager.load_config_from_file(config_file_path=remote_config_path)

            return remote_config["version_number"]
        except Exception:
            return ""
        finally:
            if os.path.exists(remote_config_path):
                os.remove(remote_config_path)

    @staticmethod
    def __compare_version_numbers_and_print_message(version_number: str, remote_version_number: str) -> None:
        if not version_number or "." not in version_number:
            print("WARNING: Could not check whether or not your version of VacuumWorld is up-to-date because the version number is malformed.\n")

            return

        print("VacuumWorld version: {}.\n".format(version_number))

        if not remote_version_number or "." not in remote_version_number:
            print("WARNING: Could not check whether or not your version of VacuumWorld is up-to-date because it was not possible to get a well formed latest version number.\n")
        elif VacuumWorld.__outdated(version_number=version_number, remote_version_number=remote_version_number):
            print("WARNING: Your version of VacuumWorld is outdated. The latest version is {}.\n".format(remote_version_number))
        else:
            print("Your version of VacuumWorld is up-to-date.\n")

    @staticmethod
    def __outdated(version_number: str, remote_version_number: str) -> bool:
        assert version_number and remote_version_number
        assert "." in version_number and "." in remote_version_number

        version_number_parts: List[str] = version_number.split(".")
        remote_version_number_parts: List[str] = remote_version_number.split(".")

        for i in range(len(version_number_parts)):
            if int(version_number_parts[i]) < int(remote_version_number_parts[i]):
                return True
            elif int(version_number_parts[i]) > int(remote_version_number_parts[i]):
                return False

        return False

    def __run(self, runner_type: Type[VWRunner], minds: Dict[VWColour, VWActorMindSurrogate], **kwargs) -> None:
        try:
            runner: VWRunner = runner_type(config=self.__config, minds=minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, **kwargs)
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
    def __process_minds(default_mind: VWActorMindSurrogate=None, white_mind: VWActorMindSurrogate=None, green_mind: VWActorMindSurrogate=None, orange_mind: VWActorMindSurrogate=None) -> Dict[VWColour, VWActorMindSurrogate]:
        assert default_mind is not None or white_mind is not None and green_mind is not None and orange_mind is not None

        if all(m is not None for m in [default_mind, white_mind, green_mind, orange_mind]):
            print("WARNING: You have specified a default mind surrogate and a mind surrogate for each of the agent colours. The default mind surrogate will be ignored.")

        # The minds are validated at a later stage.
        return {
            VWColour.white: white_mind if white_mind is not None else default_mind,
            VWColour.green: green_mind if green_mind is not None else default_mind,
            VWColour.orange: orange_mind if orange_mind is not None else default_mind
        }

    @staticmethod
    def __set_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal_module, "SIGTSTP"):
            from signal import SIGTSTP

            handle_signal(SIGTSTP, lambda _, __: print("SIGTSTP received and ignored."))


# For back-compatibility with 4.2.5.
def run(default_mind: VWActorMindSurrogate=None, white_mind: VWActorMindSurrogate=None, green_mind: VWActorMindSurrogate=None, orange_mind: VWActorMindSurrogate=None, **kwargs) -> None:
    vw: VacuumWorld = VacuumWorld()
    vw.run(default_mind=default_mind, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, **kwargs)
