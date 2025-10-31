from typing import Type, Optional, Any, cast
from sys import version_info
from traceback import print_exc
from signal import signal as handle_signal
from requests import get, Response
from time import sleep
from screeninfo import get_monitors as get_monitors_with_screeninfo, ScreenInfoError
from pymonitors import get_monitors as get_monitors_with_pymonitors
from pyoptional.pyoptional import PyOptional
from subprocess import call
from tempfile import mkdtemp, mkstemp
from tomllib import load as load_toml
from shutil import rmtree
from importlib.metadata import version

from pystarworldsturbo.utils.json.json_value import JSONValue

from .vwconfig_manager import VWConfigManager
from .model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from .model.actor.mind.surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from .common.vwuser_difficulty import VWUserDifficulty
from .common.vwcolour import VWColour
from .common.vwexceptions import VWInternalError, VWRunnerException
from .runner.vwrunner import VWRunner
from .runner.vwgui_runner import VWGUIRunner
from .runner.vwguiless_runner import VWGUIlessRunner

import os
import signal as signal_module


class VacuumWorld():
    CONFIG_FILE_NAME: str = "config.json"
    CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)
    MIN_PYTHON_VERSION: tuple[int, int] = (3, 13)
    ALLOWED_RUN_ARGS: dict[str, Type[Any]] = {
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
        "efforts": dict[str, int],
        "total_cycles": int,
        "randomness_enabled": bool
    }

    def __init__(self) -> None:
        VacuumWorld.__python_version_check()
        VacuumWorld.__set_sigtstp_handler()

        self.__config: dict[str, JSONValue] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)

        self.__config["version_number"] = version("vacuumworld")

        self.__vw_version_check()

    def run(self, default_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), white_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), green_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), orange_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), **kwargs: Any) -> None:
        '''
        Loads the mind surrogates, and selects the appropriate VacuumWorld runner. Then, it loads the configuration options, and starts the loaded runner.
        '''
        minds: dict[VWColour, VWActorMindSurrogate] = VacuumWorld.__process_minds(default_mind=default_mind, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind)
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
            if len(get_monitors_with_screeninfo()) > 0:
                return True
            else:
                raise ScreenInfoError("No monitor found by `screeninfo`.")
        except Exception:
            for monitor in get_monitors_with_pymonitors(print_info=False):
                if monitor.data["successfully_parsed"] and all(dimension in monitor.data for dimension in ["width", "height"]) and monitor.data["width"] > 0 and monitor.data["height"] > 0:
                    return True

            return False

    @staticmethod
    def __python_version_check() -> None:
        if VacuumWorld.__unsupported_python_version():
            print(f"VacuumWorld requires Python {VacuumWorld.MIN_PYTHON_VERSION[0]}.{VacuumWorld.MIN_PYTHON_VERSION[1]} or later. Please install Python {VacuumWorld.MIN_PYTHON_VERSION[0]}.{VacuumWorld.MIN_PYTHON_VERSION[1]} or later and try again.")

            exit(1)
        else:
            print(f"Python version: {version_info.major}.{version_info.minor}.{version_info.micro}. Good!")

    @staticmethod
    def __unsupported_python_version() -> bool:
        if version_info.major < VacuumWorld.MIN_PYTHON_VERSION[0]:
            return True
        elif version_info.major == VacuumWorld.MIN_PYTHON_VERSION[0] and version_info.minor < VacuumWorld.MIN_PYTHON_VERSION[1]:
            return True
        else:
            return False

    def __vw_version_check(self) -> None:
        version_number: str = cast(str, self.__config["version_number"])
        remote_version_number: str = self.__get_remote_version_number()

        outdated: bool = self.__compare_version_numbers_and_print_message(version_number, remote_version_number)

        if outdated:
            self.__attempt_auto_update()

    def __attempt_auto_update(self) -> None:
        print("Attempting to update VacuumWorld automatically...")

        temp_dir: str = mkdtemp(prefix="vacuumworld_update_")
        cloning_command: list[str] = ["git", "clone", cast(str, self.__config["project_repo_url"]), "--depth", "1", temp_dir]
        pip_command: list[str] = ["pip", "install", "--upgrade", temp_dir]

        try:
            result: int = call(cloning_command)

            if result != 0:
                raise IOError()

            result = call(pip_command)

            if result != 0:
                raise IOError()

            print("Done.")
        except Exception:
            print("WARNING: Could not update VacuumWorld automatically. Please update VacuumWorld manually.")
        finally:
            if os.path.exists(temp_dir):
                rmtree(temp_dir)

    def __download_remote_pyproject(self) -> str:
        """
        Downloads the remote pyproject.toml from the GitHub repository (raw content)
        and stores it temporarily. Returns the local file path, or an empty string on failure.
        """
        try:
            remote_toml_url = f"{self.__config["project_repo_raw_content_url"]}pyproject.toml"

            fd, temp_path = mkstemp(prefix="vacuumworld_remote_pyproject_", suffix=".toml")

            os.close(fd)

            response: Response = get(remote_toml_url, allow_redirects=True, timeout=5)
            response.raise_for_status()

            with open(temp_path, "w", encoding="utf-8") as remote_file:
                remote_file.write(response.text)

            return temp_path

        except Exception:
            return ""

    def __get_remote_version_number(self) -> str:
        '''
        Reads the [project].version field from the remote pyproject.toml.

        Returns the version string, or "" on failure.
        '''
        remote_path: str = self.__download_remote_pyproject()

        if not remote_path:
            return ""

        try:
            with open(remote_path, "rb") as i_f:
                pyproject_data: dict[str, Any] = load_toml(i_f)

            project_data: dict[str, Any] = pyproject_data.get("project", {})
            version: str = project_data.get("version", "")

            os.remove(remote_path)

            return version
        except Exception:
            try:
                os.remove(remote_path)
            except OSError:
                pass

            return ""

    def __compare_version_numbers_and_print_message(self, version_number: str, remote_version_number: str) -> bool:
        if not version_number or "." not in version_number:
            print("WARNING: Could not check whether or not your version of VacuumWorld is up-to-date because the version number is malformed.\n")

            return True  # Conservative approach (i.e., consider VW outdated).

        print(f"VacuumWorld version (local): {version_number}.")
        print(f"VacuumWorld version (remote): {remote_version_number}.\n")

        if not remote_version_number or "." not in remote_version_number:
            print("WARNING: Could not check whether or not your version of VacuumWorld is up-to-date because it was not possible to get a well formed latest version number.\n")

            return True  # Conservative approach (i.e., consider VW outdated).
        elif VacuumWorld.__outdated(version_number=version_number, remote_version_number=remote_version_number):
            print(f"WARNING: Your version of VacuumWorld is outdated. The latest version is {remote_version_number}.\n")

            return True
        else:
            print("Your version of VacuumWorld is up-to-date.\n")

            return False

    @staticmethod
    def __outdated(version_number: str, remote_version_number: str) -> bool:
        assert version_number and remote_version_number
        assert "." in version_number and "." in remote_version_number

        version_number_parts: list[str] = version_number.split(".")
        remote_version_number_parts: list[str] = remote_version_number.split(".")

        for i in range(len(version_number_parts)):
            if int(version_number_parts[i]) < int(remote_version_number_parts[i]):
                return True
            elif int(version_number_parts[i]) > int(remote_version_number_parts[i]):
                return False

        return False

    def __run(self, runner_type: Type[VWRunner], minds: dict[VWColour, VWActorMindSurrogate], **kwargs: Any) -> None:
        runner: PyOptional[VWRunner] = self.__get_runner(runner_type=runner_type, minds=minds, **kwargs)

        try:
            if runner.is_present():
                runner.or_else_raise().start()
                runner.or_else_raise().join()
            else:
                raise VWRunnerException("Could not create runner.")
        except KeyboardInterrupt:
            print("Received a SIGINT (possibly via CTRL+C). Stopping...")

            if runner.is_present():
                runner.or_else_raise().propagate_stop_signal()
                runner.or_else_raise().join()
        except VWRunnerException:
            print("ERROR: Could not create runner. Please check the error message above.")
        except VWInternalError:
            print("ERROR: An internal error occurred. Please check the error message above.")
        except Exception:
            print_exc()
            print("Fatal error. Bye")

    def __get_runner(self, runner_type: Type[VWRunner], minds: dict[VWColour, VWActorMindSurrogate], **kwargs: Any) -> PyOptional[VWRunner]:
        try:
            return PyOptional[VWRunner].of(runner_type(config=self.__config, minds=minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, **kwargs))
        except VWRunnerException as e:
            print(f"ERROR: {e.args[0] if len(e.args) > 0 and e.args[0] else 'Unknown error.'}\n")

            return PyOptional[VWRunner].empty()
        except Exception:
            print("Unkonwn error.\n")
            print_exc()

            return PyOptional[VWRunner].empty()

    @staticmethod
    def __process_minds(default_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), white_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), green_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty(), orange_mind: PyOptional[VWActorMindSurrogate]=PyOptional.empty()) -> dict[VWColour, VWActorMindSurrogate]:
        if default_mind.is_empty() and any(m.is_empty() for m in [white_mind, green_mind, orange_mind]):
            raise ValueError("You must provide a `default_mind` surrogate, or all coloured mind surrogates (i.e., `green_mind`, `orange_mind`, and `white_mind`).")

        if all(m.is_present() for m in [default_mind, white_mind, green_mind, orange_mind]):
            print("WARNING: You have specified a `default_mind` surrogate and a mind surrogate for each of the agent colours. The `default_mind` surrogate will be ignored.")

        # The minds are validated at a later stage.
        return {
            VWColour.white: white_mind.or_else_raise() if white_mind.is_present() else default_mind.or_else_raise(),
            VWColour.green: green_mind.or_else_raise() if green_mind.is_present() else default_mind.or_else_raise(),
            VWColour.orange: orange_mind.or_else_raise() if orange_mind.is_present() else default_mind.or_else_raise()
        }

    @staticmethod
    def __set_sigtstp_handler() -> None:
        # Safeguard against crashes on Windows and every other OS without SIGTSTP.
        if hasattr(signal_module, "SIGTSTP"):
            from signal import SIGTSTP

            handle_signal(SIGTSTP, lambda num, _: print(f"SIGTSTP (signal number {num}) received and ignored."))


def run(default_mind: Optional[VWActorMindSurrogate]=None, white_mind: Optional[VWActorMindSurrogate]=None, green_mind: Optional[VWActorMindSurrogate]=None, orange_mind: Optional[VWActorMindSurrogate]=None, **kwargs: Any) -> None:
    '''
    The entry point of VacuumWorld.

    Arguments:

    - `default_mind`: the mind surrogate to be used by all agents, if no specific mind surrogate is provided for them. This argument is mandatory, unless all of the following arguments are provided: `white_mind`, `green_mind`, and `orange_mind`.

    - `green_mind`: the mind surrogate to be used by all green agent. If not provided, `default_mind` will be used.

    - `orange_mind`: the mind surrogate to be used by all orange agent. If not provided, `default_mind` will be used.

    - `white_mind`: the mind surrogate to be used by all white agents. If not provided, `default_mind` will be used.

    - `gui`: if `True`, the GUI will be used. If `False`, the GUI will not be used. If not provided, the GUI will be used if a display is available, and not used otherwise. Please note that `load` must be provided if `gui` is `False`, or if no displays are available.

    - `skip`: if `True`, the initial GUI window will be skipped. If `False`, it will not be skipped. If not provided, it will not be skipped. Please note that this argument is only relevant if `gui` is `True`.

    - `play`: must be used in conjunction with `load`. If `True`, the simulation will start automatically (past the initial window) with the provided state. If `False`, the simulation will not start automatically. If not provided, the simulation will not start automatically.

    - `load`: the path to a file containing a state to be loaded. If not provided, an empty gird will be loaded. In both cases, the grid can be further customised via the GUI (unless a `play` is provided with a `True` value).

    - `speed`: the `float` speed modifier of the simulation. It must be `>= 0` and `< 1`. The higher the number, the lower the latency between cycles. If not provided, `0` will be used. *WARNING*: Python will approximate a value with too many 9s to 1 (e.g., 0.99999999999999999999).

    - `scale`: the `float` scale modifier of the GUI. It must be `>= 0`. It must be `>= 0` and `< 2.5`. The higher the number, the bigger the GUI. If not provided, `1` will be used. A `0` value will be ignored, and `1` will be used.

    - `tooltips`: if `True`, the button tooltips will be shown. If `False`, tooltips will not be shown. If not provided, tooltips will be shown.

    - `efforts`: a `dict[str, int]` containing the efforts of each action type. The keys are the action names, and the values are the efforts. If not provided, the default efforts will be used.

    - `total_cycles`: the total number of cycles to be executed. It must be `> 0`. If not provided, the simulation will run indefinitely. A `0` value will be ignored, and the simulation will run indefinitely.
    '''
    # The use of `Optional` instead of `PyOptional` for the arguments is intentional, so that the user can avoid wrapping the minds in `PyOptional`.
    vw: VacuumWorld = VacuumWorld()

    vw.run(default_mind=PyOptional[VWActorMindSurrogate].of_nullable(default_mind), white_mind=PyOptional[VWActorMindSurrogate].of_nullable(white_mind), green_mind=PyOptional[VWActorMindSurrogate].of_nullable(green_mind), orange_mind=PyOptional[VWActorMindSurrogate].of_nullable(orange_mind), **kwargs)
