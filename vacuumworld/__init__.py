from .model.actor.user_mind_surrogate import UserMindSurrogate
from .model.actor.user_difficulty import UserDifficulty
from .common.colour import Colour
from .gui.gui import VWGUI
from .utils.vwutils import process_minds

from signal import signal, SIGTSTP, SIG_IGN
from json import load
from screeninfo import get_monitors

import os



# __all__: list = ["run", Coord, Direction, Orientation, Colour, Observation, Location, Actor, DirtInterface, action, coord, direction, orientation, colour, observation, location, actor, dirt]

CONFIG_FILE_PATH: str = "config.json"



def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs) -> None:
    if hasattr(signal, "SIGTSTP"): # To exclude Windows and every OS without SIGTSTP.
        signal(SIGTSTP, SIG_IGN)

    white_mind, green_mind, orange_mind = process_minds(default_mind, white_mind, green_mind, orange_mind)

    config: dict = load_config()

    user_mind: UserMindSurrogate = UserMindSurrogate(difficulty_level=UserDifficulty(config["default_user_mind_level"]))

    vwgui: VWGUI = VWGUI(config=config)

    try:
        vwgui.init_gui_conf(minds={Colour.white: white_mind, Colour.green: green_mind, Colour.orange: orange_mind, Colour.user: user_mind}, **kwargs)
        vwgui.start()
        vwgui.join()
    except KeyboardInterrupt:
        print("Received a SIGINT (possibly via CTRL+C). Stopping...")
        vwgui.kill()
        vwgui.join()


def load_config() -> dict:
    with open(CONFIG_FILE_PATH, "r") as f:
        config: dict = load(fp=f)
    
    # TODO: check the monitor number, rather than using the default one.
    config["screen_width"] = get_monitors()[config["default_monitor_number"]].width
    config["screen_height"] = get_monitors()[config["default_monitor_number"]].height
    config["x_scale"] = float(config["screen_width"] / config["base_screen_width"])
    config["y_scale"] = float(config["screen_height"] / config["base_screen_height"])

    if config["screen_height"] < config["screen_width"]:
        config["scale"] = config["y_scale"]
    else:
        config["scale"] = config["x_scale"]

    top_directory_path: str = os.path.join(os.getcwd(), config["top_directory_name"])
    config["button_images_path"] = os.path.join(top_directory_path, config["res_directory_name"])
    config["location_agent_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["agent_images_directory_name"])
    config["location_dirt_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["dirt_images_directory_name"])
    config["main_menu_image_path"] = os.path.join(top_directory_path, config["res_directory_name"], "start_menu.png")

    for entry in config["to_compute_programmatically_at_boot"]:
        assert entry and entry != -1

    return config
