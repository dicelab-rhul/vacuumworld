from signal import signal, SIG_IGN
from json import load
from screeninfo import get_monitors
from typing import List, Tuple

from .config_manager import ConfigManager
from .model.actions.vwactions import VWAction
from .model.actions.effort import ActionEffort
from .model.actor.actor_mind_surrogate import ActorMindSurrogate
from .model.actor.user_mind_surrogate import UserMindSurrogate
from .model.actor.user_difficulty import UserDifficulty
from .common.colour import Colour
from .gui.gui import VWGUI
from .guiless import VWGuilessRunner

import vacuumworld.common
import vacuumworld.gui
import vacuumworld.model
import vacuumworld.res

import os


__all__: List[str] = [vacuumworld.common, vacuumworld.gui, vacuumworld.model, vacuumworld.res]

CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
    # Safeguard against crashes on Windows and every other OS without SIGTSTP.
    if hasattr(signal, "SIGTSTP"):
        from signal import SIGTSTP

        signal(SIGTSTP, SIG_IGN)

    __assign_efforts_to_actions(**kwargs)

    white_mind, green_mind, orange_mind = __process_minds(default_mind, white_mind, green_mind, orange_mind)

    config: dict = ConfigManager(config_file_path=CONFIG_FILE_PATH).load_config()

    user_mind: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty(config["default_user_mind_level"]))

    if "gui" in kwargs and not kwargs.get("gui"):
        __run_guiless(config=config, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)
    else:
        __run_with_gui(config=config, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)


def __assign_efforts_to_actions(**kwargs) -> None:
    if "efforts" in kwargs and type(kwargs["efforts"]) == dict:
        for k, v in kwargs["efforts"].items():
            if type(k) == type and issubclass(k, VWAction) and type(v) == int:
                ActionEffort.override_default_effort_for_action(action_name=k.__name__, new_effort=v)

                print("The effort of {} is now {}.".format(k.__name__, ActionEffort.EFFORTS[k.__name__]))


def __run_guiless(config: dict, white_mind: ActorMindSurrogate, green_mind: ActorMindSurrogate, orange_mind: ActorMindSurrogate, user_mind: UserMindSurrogate, **kwargs) -> None:
    if "load" not in kwargs or not kwargs.get("load"):
        print("VacuumWorld cannot run GUI-less if no savestate file is provided.")
    else:
        print("RunningGUI-less...")
        vw_runner: VWGuilessRunner = VWGuilessRunner(config=config, minds={Colour.white: white_mind, Colour.green: green_mind, Colour.orange: orange_mind, Colour.user: user_mind}, load=kwargs.get("load"))
        vw_runner.start()


def __run_with_gui(config: dict, white_mind: ActorMindSurrogate, green_mind: ActorMindSurrogate, orange_mind: ActorMindSurrogate, user_mind: UserMindSurrogate, **kwargs) -> None:
    vwgui: VWGUI = VWGUI(config=config)

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


def __process_minds(default_mind: ActorMindSurrogate=None, white_mind: ActorMindSurrogate=None, green_mind: ActorMindSurrogate=None, orange_mind: ActorMindSurrogate=None) -> Tuple[ActorMindSurrogate, ActorMindSurrogate, ActorMindSurrogate]:
    assert default_mind is not None or white_mind is not None and green_mind is not None and orange_mind is not None

    if white_mind is None:
        white_mind = default_mind

    if green_mind is None:
        green_mind = default_mind

    if orange_mind is None:
        orange_mind = default_mind

    ActorMindSurrogate.validate(white_mind, Colour.white)
    ActorMindSurrogate.validate(green_mind, Colour.green)
    ActorMindSurrogate.validate(orange_mind, Colour.orange)

    return white_mind, green_mind, orange_mind
