from json import load
from screeninfo import get_monitors

import os


class ConfigManager():
    def __init__(self, config_file_path: str) -> None:
        self.__config_file_path: str = config_file_path

    def load_config(self) -> dict:
        with open(file=self.__config_file_path, mode="r") as f:
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
