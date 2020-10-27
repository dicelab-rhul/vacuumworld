# -*- coding: utf-8 -*-
#from vacuumworld.gui.vwv import run as run_gui
from vacuumworld.gui.gui import VWGUI
from vacuumworld.utils.vwutils import process_minds

from vacuumworld.core.common.coordinates import Coord, coord
from vacuumworld.core.common.direction import Direction, direction
from vacuumworld.core.common.orientation import Orientation, orientation
from vacuumworld.core.common.colour import Colour, colour
from vacuumworld.core.common.observation import Observation, observation
from vacuumworld.core.environment.location_interface import Location, location
from vacuumworld.core.agent.agent_interface import Agent, agent
from vacuumworld.core.dirt.dirt_interface import Dirt, dirt
from vacuumworld.core.action import action

from signal import signal, SIGTSTP, SIG_IGN
from sys import exit
from json import load
from screeninfo import get_monitors

import os



__all__ = ["run", Coord, Direction, Orientation, Colour, Observation, Location, Agent, Dirt, action, coord, direction, orientation, colour, observation, location, agent, dirt]


def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs):
    if hasattr(signal, "SIGTSTP"): # To exclude Windows and every OS without SIGTSTP.
        signal(SIGTSTP, SIG_IGN)

    white_mind, green_mind, orange_mind = process_minds(default_mind, white_mind, green_mind, orange_mind)

    config: dict = load_config()

    try:
        #run_gui({Colour.white:white_mind, Colour.green:green_mind, Colour.orange:orange_mind}, **kwargs)
        vwgui: VWGUI = VWGUI(config=config)
        vwgui.run({Colour.white:white_mind, Colour.green:green_mind, Colour.orange:orange_mind}, **kwargs)
   
    except KeyboardInterrupt:
        print("\nReceived a keyboard interrupt. Exiting...")
        exit(-1)


def load_config() -> dict:
    with open("config.json") as f: #TODO: magic string.
        config: dict = load(fp=f)

    #TODO: check the monitor number.
    config["screen_width"] = get_monitors()[0].width
    config["screen_height"] = get_monitors()[0].height
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
