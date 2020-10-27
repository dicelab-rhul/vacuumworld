from tkinter import Tk
from sys import exit, exc_info
from inspect import getsourcefile
from webbrowser import open_new_tab
from threading import Thread

from .components.frames.initial_window import VWInitialWindow
from .components.frames.simulation_window import VWSimulationWindow
from ..core.environment.vw import Grid
from ..core.common.colour import Colour
from ..utils.autocomplete import AutocompleteEntry
from ..utils.saveload import SaveStateManager
from ..utils.vwutils import ignore, VacuumWorldActionError

import traceback



class VWGUI(Thread):
    def __init__(self, config: dict) -> None:
        super(VWGUI, self).__init__()

        self.__config: dict = config
        self.__minds: dict = {}
        self.__user_mind: int = config["default_user_mind_level"]
        self.__root: Tk
        self.__initial_window: VWInitialWindow = None
        self.__simulation_window: VWSimulationWindow = None
        self.__grid: Grid = None # Programmatic representation of the VW grid (not a GUI element)
        self.__save_state_manager: SaveStateManager = SaveStateManager()
        self.__already_centered: bool = False

    def init_gui_conf(self, minds: dict, skip: bool=False, play: bool=False, speed: float=0.0, load: str=None, scale: float=0.0, tooltips: bool=True) -> None:
        try:
            assert minds is not None

            self.__minds = minds
            VWGUI.__validate_arguments(play=play, file_to_load=load, speed=speed, scale=scale)
            self.__override_default_config(skip=skip, play=play, speed=speed, file_to_load=load, scale=scale, tooltips=tooltips)
            self.__scale_config_parameters()
        except Exception as e:
            self.__clean_exit(exc=e)

    @staticmethod
    def __validate_arguments(play: bool, speed: float, file_to_load: str, scale: str) -> None:
        if play and not file_to_load:
            raise ValueError("Argument \"load\" must be specified if argument \"play\" = True") # TODO: magic strings.

        if speed < 0 or speed >= 1:
            raise ValueError("Argument \"speed\" must be >=0 and < 1.") # TODO: magic string and magic numbers.

        if scale < 0: #TODO: define and check for a sane upper bound.
            raise ValueError("Argument \"scale\" must be > 0.") # TODO: magic string and magic numbers.

    def __override_default_config(self, skip: bool=False, play: bool=False, speed: float=0.0, file_to_load: str=None, scale: float=1.0, tooltips: bool=True) -> None:
        self.__config["white_mind_filename"] = getsourcefile(self.__minds[Colour.white].__class__)
        self.__config["orange_mind_filename"] = getsourcefile(self.__minds[Colour.orange].__class__)
        self.__config["green_mind_filename"] = getsourcefile(self.__minds[Colour.green].__class__)
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
        Tk.report_callback_exception = self.__clean_exit

        self.__root = Tk()
        self.__root.title("VacuumWorld v{}".format(self.__config["version_number"]))
        self.__root.protocol("WM_DELETE_WINDOW", self.__finish)
        self.__root.configure(background=self.__config["bg_colour"])

        if self.__config["file_to_load"]:
            self.__load_grid()
        else:
            self.__create_new_grid()

        self.__show_appropriate_window()
        self.__root.after(1000, lambda:{})
        self.__root.mainloop()

    def __show_appropriate_window(self) -> None:
        if not self.__config["skip"]:
            self.__show_initial_window()
        else:
            self.__show_simulation_window()

    def __load_grid(self) -> None:
        try:
            loaded_grid: Grid = self.__load_file(file=self.__config["file_to_load"])
            self.__create_new_grid(dim=loaded_grid.dim)
            self.__grid.replace_all(grid=loaded_grid)
        except Exception:
            print("Something went wrong. Could not load any grid from {}".format(self.__config["file_to_load"]))

    def __create_new_grid(self, dim=-1) -> None:
        if dim == -1:
            dim = self.__config["initial_environment_dim"]

        self.__grid = Grid(dim=dim)

    def __show_initial_window(self) -> None:
        self.__initial_window = VWInitialWindow(root=self.__root, config=self.__config, _start=self.__start, _exit=self.__finish, _guide=self.__guide)
        self.__initial_window.pack()
        self.__center_and_adapt_to_resolution()

    def __show_simulation_window(self) -> None:
        self.__simulation_window = VWSimulationWindow(
            root=self.__root, config=self.__config, minds=self.__minds, user_mind=self.__user_mind, grid=self.__grid,
            _guide=self.__guide, _save=self.__save, _load=self.__load, _finish=self.__finish, _error=self.__clean_exit)

        self.__simulation_window.pack()
        self.__center_and_adapt_to_resolution()

        self.__root.deiconify()

        if self.__config["skip"] or self.__config["file_to_load"]:
            self.__simulation_window._redraw()
            self.__center_and_adapt_to_resolution()

        if self.__config["play"]:
            self.__simulation_window.play()

    def __clean_exit(self, *args, **kwargs) -> None:
        ignore(args)
        ignore(kwargs)
        
        _type, value, tb = exc_info()
        tb =  traceback.extract_tb(tb)
        agent_error = False

        i = 0 # As a fallback.

        for i, s in enumerate(tb):
            if s.filename in (self.__config["white_mind_filaname"], self.__config["orange_mind_filaname"], self.__config["green_mind_filaname"]):
                agent_error = True
                break
        
        agent_error = agent_error or _type == VacuumWorldActionError
        i = int(agent_error) * i

        print("Traceback:\n")
        print("".join(traceback.format_list(tb[i:])))
        print("Exception:\n")
        print("  "  + "  ".join(traceback.format_exception_only(_type, value)))

        if  self.__root is not None:
            self.__root.destroy()
            exit(-1)

    def finish(self) -> None:
        self.__finish()

    def __finish(self) -> None:
        if self.__simulation_window is not None:
            self.__simulation_window.destroy()
        
        if self.__initial_window is not None:
            self.__initial_window.destroy()

        if self.__root is not None:
            self.__root.destroy()

        exit(0)

    def __guide(self) -> None:
        open_new_tab(url=self.__config["project_repo_url"])

    def __start(self):
        if self.__initial_window:
            self.__initial_window.forget()
            self.__initial_window.destroy()
            self.__root.withdraw()

        self.__show_simulation_window()

    def __save(self, saveloadmenu: AutocompleteEntry) -> None:
        file: str = saveloadmenu.var.get()
        result: bool = self.__save_state_manager.save_state(grid=self.__grid, file=file)

        if result:
            saveloadmenu.lista = self.__save_state_manager.get_ordered_list_of_filenames_in_save_directory()
            print("The current grid was successfully saved.")
        else:
            print("The current grid was not saved.")

    def __load(self, saveloadmenu: AutocompleteEntry) -> Grid:
        file: str = saveloadmenu.var.get()
        
        return self.__load_file(file=file)

    def __load_file(self, file: str) -> Grid:
        data: Grid = self.__save_state_manager.load_state(file=file)

        if data:
            print("The saved grid was successfully loaded.")
            return data
        else:
            print("The state was not loaded.")
            return self.__create_new_grid()

    def __center_and_adapt_to_resolution(self) -> None:
        if not self.__already_centered:
            w = self.__root.winfo_reqwidth() * self.__config["x_scale"]
            h = self.__root.winfo_reqheight() * self.__config["y_scale"]
            sw = self.__root.winfo_screenwidth()
            sh = self.__root.winfo_screenheight()
            x = (sw / 2) - w - w/4 + w/26
            y = (sh / 2) - h - h/2
            self.__root.x = x
            self.__root.y = y
            self.__root.geometry("+%d+%d" % (x, y))
            self.__already_centered = True
