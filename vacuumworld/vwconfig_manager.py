from json import load
from screeninfo import get_monitors, ScreenInfoError, Monitor
from typing import Any

import os


class VWConfigManager():
    '''
    This class is responsible for loading the configuration of the application.
    '''
    @staticmethod
    def load_config_from_file(config_file_path: str) -> dict[str, Any]:
        '''
        Loads the configuration from the file identified by `config_file_path`, and returns it as a `dict`.

        This method assumes (via assertions) that `config_file_path` points to an existing file.

        If something goes wrong during the I/O operations, the resulting `IOError` is not caught (and thus automatically propagated).
        '''
        assert config_file_path and isinstance(config_file_path, str) and os.path.exists(config_file_path) and os.path.isfile(config_file_path)

        # We let the `IOError` propagate, if any.
        with open(file=config_file_path, mode="r") as f:
            config: dict[str, Any] = load(fp=f)

        try:
            # Assuming the first monitor is the one where VW is running.
            default_monitor_number: int = config["default_monitor_number"]
            monitor: Monitor = get_monitors()[default_monitor_number]

            config["screen_width"] = monitor.width
            config["screen_height"] = monitor.height
            config["x_scale"] = float(config["screen_width"] / config["base_screen_width"])
            config["y_scale"] = float(config["screen_height"] / config["base_screen_height"])

            if config["screen_height"] < config["screen_width"]:
                config["scale"] = config["y_scale"]
            else:
                config["scale"] = config["x_scale"]
        except ScreenInfoError:
            print("INFO: no monitor available.")
        finally:
            top_directory_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config["top_directory_name"])
            config["button_data_path"] = os.path.join(top_directory_path, config["res_directory_name"])
            config["location_agent_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["agent_images_directory_name"])
            config["location_dirt_images_path"] = os.path.join(top_directory_path, config["res_directory_name"], config["locations_directory_name"], config["dirt_images_directory_name"])
            config["main_menu_image_path"] = os.path.join(top_directory_path, config["res_directory_name"], "start_menu.png")

            for entry in config["to_compute_programmatically_at_boot"]:
                assert entry and entry != -1

        return config
