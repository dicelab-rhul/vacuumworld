from signal import signal, SIG_IGN
from json import load
from screeninfo import get_monitors
from typing import List, Tuple

from .model.actions.vwactions import VWAction
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

    config: dict = __load_config()

    user_mind: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty(config["default_user_mind_level"]))

    if "gui" in kwargs and not kwargs.get("gui"):
        __run_guiless(config=config, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)
    else:
        __run_with_gui(config=config, white_mind=white_mind, green_mind=green_mind, orange_mind=orange_mind, user_mind=user_mind, **kwargs)


def __assign_efforts_to_actions(**kwargs) -> None:
    if "efforts" in kwargs and type(kwargs["efforts"]) == dict:
        for k, v in kwargs["efforts"].items():
            if issubclass(k, VWAction) and type(v) == int:
                k.override_default_effort(new_effort=v)
                print("The effort of {} is now {}.".format(k.__name__, v))


def __run_guiless(config: dict, white_mind: ActorMindSurrogate, green_mind: ActorMindSurrogate, orange_mind: ActorMindSurrogate, user_mind: UserMindSurrogate, **kwargs) -> None:
    if not "load" in kwargs or not kwargs.get("load"):
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


def __load_config() -> dict:
    with open(CONFIG_FILE_PATH, "r") as f:
        config: dict = load(fp=f)

    # Assuming the first monitor is the one where VW is running.
    config["screen_width"] = get_monitors()[config["default_monitor_number"]].width
    config["screen_height"] = get_monitors()[config["default_monitor_number"]].height
    config["x_scale"] = float(config["screen_width"] / config["base_screen_width"])
    config["y_scale"] = float(config["screen_height"] / config["base_screen_height"])

    if config["screen_height"] < config["screen_width"]:
        config["scale"] = config["y_scale"]
    else:
        config["scale"] = config["x_scale"]

    top_directory_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config["top_directory_name"])
    config["button_data_path"] = os.path.join(top_directory_path, config["res_directory_name"])
    config["location_agent_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["agent_images_directory_name"])
    config["location_dirt_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["dirt_images_directory_name"])
    config["main_menu_image_path"] = os.path.join(top_directory_path, config["res_directory_name"], "start_menu.png")

    for entry in config["to_compute_programmatically_at_boot"]:
        assert entry and entry != -1

    return config


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
