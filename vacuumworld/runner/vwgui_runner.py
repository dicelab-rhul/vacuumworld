from typing import Type, Any
from tkinter import Tk
from webbrowser import open_new_tab
from json import load
from math import floor

from .vwrunner import VWRunner
from ..gui.components.vwautocomplete import VWAutocompleteEntry
from ..gui.components.frames.vwinitial_window import VWInitialWindow
from ..gui.components.frames.vwsimulation_window import VWSimulationWindow
from ..common.vwcolour import VWColour
from ..model.environment.vwenvironment import VWEnvironment
from ..model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate

import os


class VWGUIRunner(VWRunner):
    '''
    This class is responsible for running VacuumWorld with a GUI.

    The VacuumWorld GUI is built on the top of the `tkinter` library.
    '''
    def __init__(self, config: dict[str, Any], minds: dict[VWColour, VWActorMindSurrogate], allowed_args: dict[str, Type[Any]], **kwargs: Any) -> None:
        super(VWGUIRunner, self).__init__(config=config, minds=minds, allowed_args=allowed_args, **kwargs)

        self.__button_data: dict[str, dict[str, str]] = self.__load_button_data()
        self.__already_centered: bool = False

    def run(self) -> None:
        '''
        Constructs the GUI and runs the simulation.

        If a `KeyboardInterrupt` is raised, the GUI is closed and the simulation is stopped.

        If any other `Exception` is raised, the GUI is closed, the simulation is stopped, and the error message is passed to the user.
        '''
        try:
            self.__root: Tk = Tk()
            self.__root.title(f"VacuumWorld v{self.get_config()['version_number']}")
            self.__root.protocol("WM_DELETE_WINDOW", self.kill)
            self.__root.configure(background=self.get_config()["bg_colour"])

            # A fresh one will be created if there is nothing to load.
            env: VWEnvironment = self.load_env()

            self.__show_appropriate_window(env=env)
            self.__loop()
        except KeyboardInterrupt:
            return
        except Exception:
            self.clean_exit()

    def __loop(self) -> None:
        while not self.must_stop_now():  # This is for external interrupts (e.g., `KeyboardInterrupt`).
            if self.can_loop():  # This is for internal interrupts (e.g., any `Exception`).
                self.__root.update_idletasks()
                self.__root.update()
            else:
                break

    def __show_appropriate_window(self, env: VWEnvironment) -> None:
        if not self.get_config()["skip"]:
            self.__show_initial_window(env=env)
        else:
            self.__show_simulation_window(env=env)

    def __show_initial_window(self, env: VWEnvironment) -> None:
        self.__initial_window: VWInitialWindow = VWInitialWindow(parent=self.__root, config=self.get_config(), buttons=self.__button_data, env=env, _start=self.__start, _exit=self.__finish, _guide=self.__guide)
        self.__initial_window.pack()

        self.__center_and_adapt_to_resolution()

    def __show_simulation_window(self, env: VWEnvironment) -> None:
        simulation_window: VWSimulationWindow = VWSimulationWindow(parent=self.__root, config=self.get_config(), buttons=self.__button_data, minds=self.get_minds(), env=env, _guide=self.__guide, _save=self.__save, _load=self.__load, _exit=self.__finish, _error=self.clean_exit)
        simulation_window.pack()

        self.__center_and_adapt_to_resolution()

        self.__root.deiconify()

        if self.get_config()["skip"] or self.get_config()["file_to_load"]:
            simulation_window.redraw()

            self.__center_and_adapt_to_resolution()

        if self.get_config()["play"]:
            simulation_window.play()

    def __finish(self) -> None:
        self.kill()

    def __guide(self) -> None:
        open_new_tab(url=self.get_config()["project_wiki_url"])

    def __start(self, env: VWEnvironment) -> None:
        if hasattr(self, f"_{type(self).__name__}__initial_window") and self.__initial_window:
            self.__initial_window.forget()
            self.__initial_window.destroy()
            self.__root.withdraw()

        self.__show_simulation_window(env=env)

    def __save(self, env: VWEnvironment, saveloadmenu: VWAutocompleteEntry) -> None:
        filename: str = saveloadmenu.get_var().get()
        result: bool = self.get_save_state_manager().save_state(env=env, filename=filename)

        if result:
            saveloadmenu.set_list_a(list_a=self.get_save_state_manager().get_ordered_list_of_filenames_in_save_directory())

            print("The current grid was successfully saved.")
        else:
            print("The current grid was not saved.")

    def __load(self, saveloadmenu: VWAutocompleteEntry) -> VWEnvironment:
        filename: str = saveloadmenu.get_var().get()

        data: dict[str, Any] = self.get_save_state_manager().load_state(filename=filename)

        return VWEnvironment.from_json(data=data, config=self.get_config())

    def __center_and_adapt_to_resolution(self) -> None:
        if not self.__already_centered:
            w: int = self.__root.winfo_reqwidth() * self.get_config()["x_scale"]
            h: int = self.__root.winfo_reqheight() * self.get_config()["y_scale"]
            sw: int = self.__root.winfo_screenwidth()
            sh: int = self.__root.winfo_screenheight()
            x: int = floor((sw / 2) - w - w/4 + w/26)
            y: int = floor((sh / 2) - h - h/2)

            self.__root.geometry("+%d+%d" % (x, y))
            self.__already_centered = True

    def __load_button_data(self) -> dict[str, dict[str, str]]:
        with open(os.path.join(str(self.get_config()["button_data_path"]), str(self.get_config()["button_data_file"])), "r") as f:
            return load(fp=f)
