from tkinter import Tk
from inspect import getsourcefile
from webbrowser import open_new_tab
from typing import Dict
from multiprocessing import Process, Event
from multiprocessing.synchronize import Event as EventType
from json import load
from signal import signal, SIGINT, SIG_IGN
from traceback import print_exc

from .components.autocomplete import AutocompleteEntry
from .components.frames.initial_window import VWInitialWindow
from .components.frames.simulation_window import VWSimulationWindow
from .saveload import SaveStateManager

from ..common.colour import Colour
from ..model.actor.actor_mind_surrogate import ActorMindSurrogate
from ..model.environment.vwenvironment import VWEnvironment

import os


class VWGUI(Process):
    def __init__(self, config: dict) -> None:
        super(VWGUI, self).__init__()

        self.__root: Tk = None
        self.__config: dict = config
        self.__button_data: dict = None
        self.__minds: Dict[Colour, ActorMindSurrogate] = {}
        self.__initial_window: VWInitialWindow = None
        self.__simulation_window: VWSimulationWindow = None
        self.__save_state_manager: SaveStateManager = SaveStateManager()
        self.__already_centered: bool = False
        self.__forceful_stop: bool = False
        self.__exit: EventType = Event()

    def propagate_stop_signal(self) -> None:
        self.__exit.set()

    def kill(self) -> None:
        self.__forceful_stop = True

    def init_gui_conf(self, minds: Dict[Colour, ActorMindSurrogate], skip: bool=False, play: bool=False, speed: float=0.0, load: str=None, scale: float=0.0, tooltips: bool=True, **_) -> None:
        try:
            assert minds

            self.__minds: Dict[Colour, ActorMindSurrogate] = minds

            VWGUI.__validate_arguments(play=play, file_to_load=load, speed=speed, scale=scale)

            self.__override_default_config(skip=skip, play=play, speed=speed, file_to_load=load, scale=scale, tooltips=tooltips)
            self.__scale_config_parameters()
            self.__button_data = self.__load_button_data()
        except Exception:
            self.__clean_exit()

    @staticmethod
    def __validate_arguments(play: bool, speed: float, file_to_load: str, scale: str) -> None:
        if play and not file_to_load:
            raise ValueError("Argument \"load\" must be specified if argument \"play\" = True")

        if speed < 0 or speed >= 1:
            raise ValueError("Argument \"speed\" must be >=0 and < 1.")

        # A 0 value is equivalent to omitting the argument from `vacuumworld.run()`.
        if scale < 0 or scale >= 2.5:
            raise ValueError("Argument \"scale\" must be >= 0 and <= 2.5.")

    def __override_default_config(self, skip: bool=False, play: bool=False, speed: float=0.0, file_to_load: str=None, scale: float=1.0, tooltips: bool=True) -> None:
        self.__config["white_mind_filename"] = getsourcefile(self.__minds[Colour.white].__class__)
        self.__config["orange_mind_filename"] = getsourcefile(self.__minds[Colour.orange].__class__)
        self.__config["green_mind_filename"] = getsourcefile(self.__minds[Colour.green].__class__)
        self.__config["user_mind_filename"] = getsourcefile(self.__minds[Colour.user].__class__)
        self.__config["skip"] |= skip
        self.__config["play"] |= play
        self.__config["time_step_modifier"] = 1 - speed

        if file_to_load:
            self.__config["file_to_load"] = file_to_load

        if scale != 0:
            self.__config["scale"] = scale
            self.__config["x_scale"] = scale
            self.__config["y_scale"] = scale

        self.__config["tooltips"] &= tooltips

    def __scale_config_parameters(self) -> None:
        self.__config["grid_size"] *= self.__config["scale"]
        self.__config["button_size"] *= self.__config["scale"]
        self.__config["location_size"] *= self.__config["scale"]
        self.__config["root_font"][1] = int(self.__config["root_font"][1] * self.__config["scale"])
        self.__config["time_step"] = self.__config["time_step"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

    def run(self) -> None:
        try:
            signal(SIGINT, SIG_IGN)

            # Safeguard against crashes on Windows and every other OS without SIGTSTP.
            if hasattr(signal, "SIGTSTP"):
                from signal import SIGTSTP

                signal(SIGTSTP, SIG_IGN)

            self.__root: Tk = Tk()
            self.__root.title("VacuumWorld v{}".format(self.__config["version_number"]))
            self.__root.protocol("WM_DELETE_WINDOW", self.kill)
            self.__root.configure(background=self.__config["bg_colour"])

            # A fresh one will be created if there is nothing to load.
            env: VWEnvironment = self.__load_env()

            self.__show_appropriate_window(env=env)
            self.__loop()
        except Exception:
            self.__clean_exit()

    def __loop(self) -> None:
        while not self.__exit.is_set():
            if self.__forceful_stop:
                break
            else:
                self.__root.update_idletasks()
                self.__root.update()

    def __show_appropriate_window(self, env: VWEnvironment) -> None:
        if not self.__config["skip"]:
            self.__show_initial_window(env=env)
        else:
            self.__show_simulation_window(env=env)

    def __load_env(self) -> VWEnvironment:
        try:
            data: dict = {}

            if self.__config["file_to_load"]:
                data = self.__load_grid_data_from_file(filename=self.__config["file_to_load"])

            return VWEnvironment.from_json(data=data, config=self.__config)
        except Exception:
            if self.__config["file_to_load"] not in (None, ""):
                print("Something went wrong. Could not load any grid from {}".format(self.__config["file_to_load"]))
            else:
                print("Something went wrong. Could not load any grid.")

            return VWEnvironment.generate_empty_env(config=self.__config)

    def __show_initial_window(self, env: VWEnvironment) -> None:
        self.__initial_window: VWInitialWindow = VWInitialWindow(parent=self.__root, config=self.__config, buttons=self.__button_data, env=env, _start=self.__start, _exit=self.__finish, _guide=self.__guide)
        self.__initial_window.pack()
        self.__center_and_adapt_to_resolution()

    def __show_simulation_window(self, env: VWEnvironment) -> None:
        self.__simulation_window: VWSimulationWindow = VWSimulationWindow(parent=self.__root, config=self.__config, buttons=self.__button_data, minds=self.__minds, env=env, _guide=self.__guide, _save=self.__save, _load=self.__load, _error=self.__clean_exit)

        self.__simulation_window.pack()
        self.__center_and_adapt_to_resolution()

        self.__root.deiconify()

        if self.__config["skip"] or self.__config["file_to_load"]:
            self.__simulation_window.redraw()
            self.__center_and_adapt_to_resolution()

        if self.__config["play"]:
            self.__simulation_window.play()

    def __clean_exit(self) -> None:
        print_exc()

        self.__finish()

    def __finish(self) -> None:
        self.kill()

    def __guide(self) -> None:
        open_new_tab(url=self.__config["project_repo_url"])

    def __start(self, env: VWEnvironment):
        if self.__initial_window:
            self.__initial_window.forget()
            self.__initial_window.destroy()
            self.__root.withdraw()

        self.__show_simulation_window(env=env)

    def __save(self, env: VWEnvironment, saveloadmenu: AutocompleteEntry) -> None:
        filename: str = saveloadmenu.var.get()
        result: bool = self.__save_state_manager.save_state(env=env, filename=filename)

        if result:
            saveloadmenu.lista = self.__save_state_manager.get_ordered_list_of_filenames_in_save_directory()
            print("The current grid was successfully saved.")
        else:
            print("The current grid was not saved.")

    def __load(self, saveloadmenu: AutocompleteEntry) -> VWEnvironment:
        filename: str = saveloadmenu.var.get()

        data: dict = self.__save_state_manager.load_state(filename=filename)

        return VWEnvironment.from_json(data=data, config=self.__config)

    def __load_grid_data_from_file(self, filename: str) -> dict:
        data: dict = self.__save_state_manager.load_state(filename=filename, no_gui=True)

        if data:
            print("The saved grid was successfully loaded.")
            return data
        else:
            print("The state was not loaded.")
            return {}

    def __center_and_adapt_to_resolution(self) -> None:
        if not self.__already_centered:
            w: int = self.__root.winfo_reqwidth() * self.__config["x_scale"]
            h: int = self.__root.winfo_reqheight() * self.__config["y_scale"]
            sw: int = self.__root.winfo_screenwidth()
            sh: int = self.__root.winfo_screenheight()
            x: int = (sw / 2) - w - w/4 + w/26
            y: int = (sh / 2) - h - h/2
            self.__root.x = x
            self.__root.y = y
            self.__root.geometry("+%d+%d" % (x, y))
            self.__already_centered = True

    def __load_button_data(self) -> dict:
        with open(os.path.join(self.__config["button_data_path"], self.__config["button_data_file"]), "r") as f:
            return load(fp=f)
