from tkinter import Event, Tk, Frame, Canvas, Label, StringVar, W, E, X
from typing import Callable, Any, cast
from PIL import Image
from PIL.Image import Image as PILImage, Resampling
from PIL.ImageTk import PhotoImage
from collections import OrderedDict
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.utils.json.json_value import JSONValue

from ..vwautocomplete import VWAutocompleteEntry
from ..buttons.vwbutton import VWButton
from ..buttons.vwdifficultybutton import VWDifficultyButton
from ..vwslider import VWSlider
from ..vwdrag_manager import VWCanvasDragManager
from ..vwbounds_manager import VWBoundsManager
from ...vwsaveload import VWSaveStateManager

from ....common.vwcoordinates import VWCoord
from ....common.vworientation import VWOrientation
from ....common.vwdirection import VWDirection
from ....common.vwcolour import VWColour
from ....common.vwexceptions import VWEndOfCyclesException
from ....model.actor.vwuser import VWUser
from ....model.actor.appearance.vwactor_appearance import VWActorAppearance
from ....model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from ....model.actor.mind.surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from ....model.actor.vwactor_factories import VWActorsFactory
from ....model.dirt.vwdirt_appearance import VWDirtAppearance
from ....common.vwuser_difficulty import VWUserDifficulty
from ....model.environment.vwenvironment import VWEnvironment
from ....model.environment.vwlocation import VWLocation

import os


class VWSimulationWindow(Frame):
    '''
    This class specifies the simulation window for the VacuumWorld GUI.

    The simulation window is the main window of the GUI. It contains the grid, the buttons, and the dragables.

    The simulation window is responsible for the following:

    * Drawing and refreshing the (visual) grid.

    * Interacting with the model (the `VWEnvironment`) to update the (visual) grid and the model itself.

    * Drawing the dragables and the buttons.

    * Handling button/dragable clicks and drags.

    * Handling key presses.

    * Handling mouse movements.
    '''
    def __init__(self, parent: Tk, config: dict[str, JSONValue], buttons: dict[str, JSONValue], minds: dict[VWColour, VWActorMindSurrogate], env: VWEnvironment, _guide: Callable[..., None], _save: Callable[..., None], _load: Callable[[VWAutocompleteEntry], VWEnvironment], _exit: Callable[..., None], _error: Callable[..., None]) -> None:
        super(VWSimulationWindow, self).__init__(parent)

        self.__parent: Tk = parent
        self.__config: dict[str, JSONValue] = config
        self.__bounds_manager: VWBoundsManager = VWBoundsManager(config=self.__config)
        # We need Any here, because we are adding lambda functions to the dict.
        self.__button_data: dict[str, Any] = buttons
        self.__env: VWEnvironment = env
        self.__guide: Callable[..., None] = _guide
        self.__save: Callable[..., None] = _save
        self.__load: Callable[[VWAutocompleteEntry], VWEnvironment] = _load
        self.__exit: Callable[..., None] = _exit
        self.__error: Callable[..., None] = _error
        self.__after_hook: PyOptional[str] = PyOptional.empty()
        self.__save_state_manager: VWSaveStateManager = VWSaveStateManager()
        self.__empty_location_coordinates_text: str = "(-,-)"
        self.__agent_minds: dict[VWColour, VWActorMindSurrogate] = minds
        self.__running: bool = False
        self.__rectangle_selected: PyOptional[int] = PyOptional.empty()
        self.__selected: PyOptional[VWCoord] = PyOptional.empty()
        self.__canvas_dirts: dict[VWCoord, int] = {}
        self.__canvas_agents: dict[VWCoord, int] = {}
        self.__all_images: dict[tuple[str, str], PILImage] = {}  # Will store all PIL images.
        self.__all_images_tk: dict[tuple[str, str], PhotoImage] = {}  # Will store all tk images.
        self.__all_images_tk_scaled: dict[tuple[str, str], PhotoImage] = {}  # Will store all tk images scaled to fit grid.
        self.__grid_lines: list[int] = []  # Will store line objects.
        self.__image_refs: list[PhotoImage] = []  # Need to keep references to PhotoImage to avoid garbage collection.

        self.__create_and_display()

        # Note: pack() for VWSimulationWindow needs to be called by the caller.

    def __create_image(self, x: int | float, y: int | float, img: PILImage | PhotoImage) -> int:
        """
        Create a Tkinter canvas image from either a PIL or PhotoImage, and
        keep a reference so it doesn't get garbage-collected.
        """
        # Ensure we have a PhotoImage
        converted_img: PhotoImage = img if isinstance(img, PhotoImage) else PhotoImage(img)

        # Keep a reference so the image persists
        if converted_img not in self.__image_refs:
            self.__image_refs.append(converted_img)

        # Create the image on the canvas
        return self.__canvas.create_image(x, y, image=converted_img)

    def __create_and_display(self) -> None:
        self.configure(background=cast(str, self.__config["bg_colour"]))

        self.__canvas: Canvas = Canvas(self, width=cast(int, self.__config["grid_size"]) + cast(int, self.__config["location_size"]) + 4, height=cast(int, self.__config["grid_size"]) + 1, bd=0, highlightthickness=0)

        self.__init_buttons()

        self.__canvas.configure(background=cast(str, self.__config["bg_colour"]))

        self.__init_images()
        self.__init_dragables()
        self.__draw_grid()

        self.__canvas.grid(row=0, column=0)  # Packing.

        # Bind keys for rotation.
        self.__parent.bind("<Left>", self.__rotate_actor_left)
        self.__parent.bind("<Right>", self.__rotate_actor_right)
        self.__parent.bind("<a>", self.__rotate_actor_left)
        self.__parent.bind("<d>", self.__rotate_actor_right)

        self.__canvas.bind("<Double-Button-1>", self.__remove_top)
        self.__canvas.bind("<Button-1>", self.__select)
        self.__canvas.bind("<Motion>", self.__on_mouse_move)
        self.__canvas.bind("<Leave>", self.__on_leave_canvas)

    def __load_button_image(self, button_name: str) -> PILImage:
        return VWSimulationWindow.__scale(Image.open(os.path.join(str(self.__config["button_data_path"]), str(self.__button_data[button_name]["image_file"]))), cast(int, self.__config["button_size"]))

    def __set_button_actions(self) -> None:
        self.__button_data["play"]["action"] = self.__play
        self.__button_data["resume"]["action"] = self.__resume
        self.__button_data["pause"]["action"] = self.__pause
        self.__button_data["stop"]["action"] = self.__stop
        self.__button_data["fast"]["action"] = self.__fast
        self.__button_data["reset"]["action"] = self.__reset
        self.__button_data["guide_bis"]["action"] = self.__guide
        self.__button_data["difficulty"]["action"] = self.__difficulty
        self.__button_data["save"]["action"] = lambda: self.__save(self.__env, self.__load_menu)
        self.__button_data["load"]["action"] = lambda: self.__load_and_redraw(self.__load_menu)

    def __build_textless_button(self, button_name: str, parent: Frame) -> VWButton:
        action: Callable[..., Any] = self.__button_data[button_name]["action"]
        image: PILImage = self.__load_button_image(button_name=button_name)
        tip_text: str = self.__button_data[button_name]["tip_text"]

        return VWButton(parent=parent, config=self.__config, img=image, fun=action, text="", tip_text=tip_text)

    def __build_difficulty_button(self, parent: Frame) -> VWDifficultyButton:
        image: PILImage = self.__load_button_image(button_name="difficulty")
        tip_text: str = self.__button_data["difficulty"]["tip_text"]

        return VWDifficultyButton(parent=parent, config=self.__config, img=image, fun=self.__difficulty, tip_text=tip_text)

    def __init_bottom_left_frame(self, bg: str) -> None:
        # Left side contains buttons and slider.
        left_frame: Frame = Frame(self.__button_frame, bg=bg)
        slider_frame: Frame = Frame(left_frame, bg=bg)
        control_buttons_frame: Frame = Frame(left_frame, bg=bg)

        for button_name in ("play", "resume", "pause", "stop", "fast", "reset", "guide_bis"):
            self.__buttons[button_name] = self.__build_textless_button(button_name=button_name, parent=control_buttons_frame)

        self.__buttons["difficulty"] = self.__build_difficulty_button(parent=control_buttons_frame)

        self.__pack_buttons("play", "reset", "fast", "difficulty", "guide_bis", forget=False)

        # Init the slider.
        self.__init_size_slider(slider_frame)

        slider_frame.grid(row=0, column=0)
        control_buttons_frame.grid(row=1, column=0, sticky=W)

        left_frame.pack(side="left", fill=X)

    def __init_saveload_frame(self, bg: str) -> None:
        # Middle contains save and load.
        self.__mid_frame: Frame = Frame(self.__button_frame, bg=bg)
        saveload_frame: Frame = Frame(self.__mid_frame, bg=bg)

        # Buttons.
        for button_name in ("save", "load"):
            self.__buttons[button_name] = self.__build_textless_button(button_name=button_name, parent=saveload_frame)

        # Entry box.
        files: list[str] = self.__save_state_manager.get_ordered_list_of_filenames_in_save_directory()
        self.__load_menu: VWAutocompleteEntry = VWAutocompleteEntry(files, 3, self.__mid_frame, font=self.__config["root_font"], bg=self.__config["autocomplete_entry_bg_colour"], fg=self.__config["fg_colour"])
        self.__load_menu.bind("<Button-1>", lambda _: self.__deselect())
        self.__load_menu.pack(side="top")

        self.__pack_buttons("save", "load", forget=False)
        saveload_frame.pack(side="bottom")
        self.__mid_frame.pack(side="left")

    def __init_info_frame(self, bg: str) -> None:
        # Init information frame.
        self.__info_frame: Frame = Frame(self.__button_frame, bg=bg)

        _size_frame: Frame = Frame(self.__info_frame, bg=bg)
        self.__size_text: StringVar = StringVar()
        self.__size_text.set(str(self.__config["initial_environment_dim"]))
        size_label: Label = Label(_size_frame, textvariable=self.__size_text, width=2, font=cast(list[str | int], self.__config["root_font"]), bg=bg, fg=cast(str, self.__config["fg_colour"]))
        size_label.grid(row=0, column=1, sticky=E)

        _size: StringVar = StringVar()
        _size.set("size:")
        _size_label: Label = Label(_size_frame, textvariable=_size, font=cast(list[str | int], self.__config["root_font"]), bg=bg, fg=cast(str, self.__config["fg_colour"]))
        _size_label.grid(row=0, column=0, sticky=W)
        _size_frame.grid(row=0, column=0, stick=W)

        self.__coordinate_text: StringVar = StringVar()
        self.__coordinate_text.set(self.__empty_location_coordinates_text)
        coordinate_label: Label = Label(self.__info_frame, textvariable=self.__coordinate_text, font=cast(list[str | int], self.__config["root_font"]), bg=bg, fg=cast(str, self.__config["fg_colour"]))
        coordinate_label.grid(row=1, column=0, sticky=W)

        self.__info_frame.pack(side="left", expand=True)
        self.__button_frame.grid(row=1, column=0, pady=3, sticky=W+E)

    def __init_buttons(self) -> None:
        self.__buttons: dict[str, VWButton] = {}

        self.__set_button_actions()

        bg: str = cast(str, self.__config["bg_colour"])

        self.__button_frame: Frame = Frame(self, bg=bg)

        self.__init_bottom_left_frame(bg=bg)
        self.__init_saveload_frame(bg=bg)
        self.__init_info_frame(bg=bg)

    def __init_size_slider(self, parent: Frame, length: int=250) -> None:
        increments: int = cast(int, self.__config["max_environment_dim"]) - cast(int, self.__config["min_environment_dim"])
        self.__grid_scale_slider: VWSlider = VWSlider(parent, self.__config, self.__on_resize, self.__on_resize_slide, length * cast(float, self.__config["scale"]), 16 * cast(float, self.__config["scale"]), slider_width=length * cast(float, self.__config["scale"]) / (increments * 3), increments=increments, start=cast(int, self.__config["grid_size"]) / cast(int, self.__config["location_size"]) - cast(int, self.__config["min_environment_dim"]))

        self.__grid_scale_slider.pack(side="top")

    def __init_dragables(self) -> None:
        # Load all images.
        keys: list[tuple[str, str]] = [("white", "north"), ("orange", "north"), ("green", "north"), ("user", "north"), ("orange", "dirt"), ("green", "dirt")]

        self.__dragables: dict[int, tuple[VWCanvasDragManager, tuple[str, str]]] = {}

        ix: int = int(cast(int, self.__config["grid_size"]) + cast(int, self.__config["location_size"]) / 2 + 2)
        iy: int = int(cast(int, self.__config["location_size"]) / 2 + 4)

        for i, key in enumerate(keys):
            item: int = self.__create_image(x=ix, y=iy + i * cast(int, self.__config["location_size"]), img=self.__all_images[key])
            drag_manager: VWCanvasDragManager = VWCanvasDragManager(self.__config, key, self.__env.get_ambient().get_grid_dim(), self.__canvas, item, self.__drag_on_start, self.__drag_on_drop)
            self.__dragables[item] = (drag_manager, key)

    def __deselect(self) -> None:
        self.__selected = PyOptional.empty()

        if self.__rectangle_selected.is_present():
            self.__canvas.delete(self.__rectangle_selected.or_else_raise())

        self.__rectangle_selected = PyOptional.empty()

    def __select(self, event: Event, print_message: bool=True) -> None:
        if not self.__running and self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            self.__deselect()
            self.focus()

            env_dim: int = self.__env.get_ambient().get_grid_dim()
            size: int = cast(int, self.__config["grid_size"])
            inc: float = size / env_dim
            x: int = min(int(event.x // inc), env_dim - 1)
            y: int = min(int(event.y // inc), env_dim - 1)
            coordinate: VWCoord = VWCoord(x=x, y=y)

            if print_message:
                print(f"SELECT: selected location {coordinate}.")

            self.__selected = PyOptional[VWCoord].of(coordinate)
            xx: float = coordinate.get_x() * inc
            yy: float = coordinate.get_y() * inc
            self.__rectangle_selected = PyOptional[int].of(self.__canvas.create_rectangle((xx + 1, yy + 1, xx + inc, yy + inc), fill="", width=3))

    def __remove_top(self, event: Event) -> None:
        if not self.__running and self.__bounds_manager.in_bounds(x=event.x, y=event.y):

            print("remove top")

            env_dim: int = self.__env.get_ambient().get_grid_dim()
            size: int = cast(int, self.__config["grid_size"])
            inc: float = size / env_dim
            x: int = min(int(event.x // inc), env_dim - 1)
            y: int = min(int(event.y // inc), env_dim - 1)
            coordinate: VWCoord = VWCoord(x=x, y=y)

            if coordinate in self.__env.get_ambient().get_grid():
                location: VWLocation = self.__env.get_ambient().get_location_interface(coord=coordinate)

                if location.has_actor():
                    actor_id: str = location.get_actor_appearance().or_else_raise().get_id()
                    # Removes the actor sprite.
                    self.__remove_actor_from_gui(coordinate)
                    # Removes the actor appearance from the grid.
                    location.remove_actor()
                    # Removes the actor from the list of actors.
                    self.__env.remove_actor(actor_id=actor_id)
                elif location.has_dirt():
                    # Removes the dirt sprite.
                    self.__remove_dirt_from_gui(coordinate)
                    # Removes both the dirt from the list of dirts, and its appearance from the grid.
                    self.__env.remove_dirt(coord=coordinate)

    # Remove an agent from the view of the grid.
    def __remove_dirt_from_gui(self, coordinate: VWCoord) -> None:
        old: int = self.__canvas_dirts[coordinate]
        self.__canvas.delete(old)
        del old

    # Remove an agent from the view of the grid.
    def __remove_actor_from_gui(self, coordinate: VWCoord) -> None:
        old: int = self.__canvas_agents[coordinate]
        self.__canvas.delete(old)
        del old

    def __rotate_actor(self, direction: VWDirection) -> None:
        if self.__selected.is_empty():
            return

        working_location: VWLocation = self.__env.get_ambient().get_location_interface(coord=self.__selected.or_else_raise())

        if working_location.has_actor():
            self.__remove_actor_from_gui(self.__selected.or_else_raise())

            new_orientation: VWOrientation = working_location.get_actor_appearance().or_else_raise().get_orientation().get(direction=direction)
            actor_colour: VWColour = working_location.get_actor_appearance().or_else_raise().get_colour()
            env_dim: int = self.__env.get_ambient().get_grid_dim()
            size: int = cast(int, self.__config["grid_size"])
            inc: float = size / env_dim
            tk_img: PhotoImage = self.__all_images_tk_scaled[(actor_colour.value, new_orientation.value)]
            item: int = self.__create_image(x=self.__selected.or_else_raise().get_x() * inc + inc/2, y=self.__selected.or_else_raise().get_y() * inc + inc/2, img=tk_img)
            self.__canvas_agents[self.__selected.or_else_raise()] = item

            self.__env.turn_actor(coord=self.__selected.or_else_raise(), direction=direction)
            self.__lines_to_front()

    def __rotate_actor_left(self, _: Any) -> None:
        self.__rotate_actor(VWDirection.left)

    def __rotate_actor_right(self, _: Any) -> None:
        self.__rotate_actor(VWDirection.right)

    def __pack_buttons(self, *buttons: str, forget: bool=True) -> None:
        if forget:
            for button in self.__buttons.values():
                button.get_button().grid_remove()
        for i in range(len(buttons)):
            self.__buttons[buttons[i]].get_button().grid(row=0, column=i, sticky=W)

    def __reset_canvas(self, lines: bool=True, dirts: bool=True, agents: bool=True, select: bool=True) -> None:
        if lines:
            for line in self.__grid_lines:
                self.__canvas.delete(line)

            self.__grid_lines.clear()
        if agents:
            for a in self.__canvas_agents.values():
                self.__canvas.delete(a)

            self.__canvas_agents.clear()
        if dirts:
            for d in self.__canvas_dirts.values():
                self.__canvas.delete(d)

            self.__canvas_dirts.clear()
        if select:
            self.__deselect()

    def __lines_to_front(self) -> None:
        for line in self.__grid_lines:
            self.__canvas.tag_raise(line)

        if self.__rectangle_selected.is_present():
            self.__canvas.tag_raise(self.__rectangle_selected.or_else_raise())

    def __load_and_redraw(self, load_menu: VWAutocompleteEntry) -> None:
        loaded_env: PyOptional[VWEnvironment] = PyOptional[VWEnvironment].empty()

        try:
            loaded_env = PyOptional[VWEnvironment].of(self.__load(load_menu))
        except Exception:
            if self.__config["file_to_load"] not in (None, ""):
                print(f"Something went wrong. Could not load any grid from {self.__config['file_to_load']}")
            else:
                print("Something went wrong. Could not load any grid.")

            loaded_env = PyOptional[VWEnvironment].of(VWEnvironment.generate_empty_env(config=self.__config))
        finally:
            if loaded_env.is_present():
                self.__redraw_loaded_env(loaded_env=loaded_env.or_else_raise())

    def __redraw_loaded_env(self, loaded_env: VWEnvironment) -> None:
        if loaded_env:
            self.__env = loaded_env
            self.__grid_scale_slider.set_position(self.__env.get_ambient().get_grid_dim() - cast(int, self.__config["min_environment_dim"]))
            self.__reset_canvas()
            self.__scaled_tk()
            self.__draw_grid()
            self.redraw()

    def redraw(self) -> None:
        '''
        This method resets and redraws the `Canvas` according to the wrapped `VWEnvironment`.
        '''
        self.__reset_canvas(lines=False)

        env_dim: int = self.__env.get_ambient().get_grid_dim()
        size: int = cast(int, self.__config["grid_size"])
        inc: float = size / env_dim

        for coord, location in self.__env.get_ambient().get_grid().items():
            if location:
                self.__redraw_location(coord=coord, location=location, inc=inc)

    def __redraw_location(self, coord: VWCoord, location: VWLocation, inc: float) -> None:
        assert location

        if location.has_actor():
            actor_appearance: VWActorAppearance = location.get_actor_appearance().or_else_raise()
            tk_img: PhotoImage = self.__all_images_tk_scaled[(actor_appearance.get_colour().value, actor_appearance.get_orientation().value)]
            item: int = self.__create_image(x=coord.get_x() * inc + inc/2, y=coord.get_y() * inc + inc/2, img=tk_img)

            self.__canvas_agents[coord] = item

            self.__canvas.tag_lower(item)  # Keep the agent behind the grid lines.

            if coord in self.__canvas_dirts:  # Keep the dirt behind the agent.
                self.__canvas.tag_lower(self.__canvas_dirts[coord])

        if location.has_dirt():
            dirt_appearance: VWDirtAppearance = location.get_dirt_appearance().or_else_raise()
            tk_img: PhotoImage = self.__all_images_tk_scaled[(dirt_appearance.get_colour().value, "dirt")]
            item: int = self.__create_image(x=coord.get_x() * inc + inc/2, y=coord.get_y() * inc + inc/2, img=tk_img)

            self.__canvas_dirts[coord] = item

            self.__canvas.tag_lower(item)  # Keep dirt behind agents and grid lines.

    def __draw_grid(self) -> None:
        env_dim: int = self.__env.get_ambient().get_grid_dim()
        size: int = cast(int, self.__config["grid_size"])

        x: float = 0.0
        y: float = 0.0
        inc: float = size / env_dim

        for _ in range(env_dim + 1):
            self.__grid_lines.append(self.__canvas.create_line(x, 0, x, size+1))
            self.__grid_lines.append(self.__canvas.create_line(0, y, size+1, y))

            y += inc
            x += inc

    @staticmethod
    def __get_image_key(name: str) -> tuple[str, str]:
        s = name.split("_")

        return (s[0], s[1])

    def __init_images(self) -> None:
        # Agents
        files: list[str] = VWSimulationWindow.__get_location_img_files(cast(str, self.__config["location_agent_images_path"]))
        image_names: list[str] = [file.split(".")[0] for file in files]

        for img_name in image_names:
            file_path: str = os.path.join(cast(str, self.__config["location_agent_images_path"]), img_name) + ".png"
            img: PILImage = VWSimulationWindow.__scale(Image.open(file_path), cast(int, self.__config["location_size"]))
            images: OrderedDict[str, PILImage] = VWSimulationWindow.__construct_images(img, img_name + "_")

            for img_name, img in images.items():
                img_key: tuple[str, str] = VWSimulationWindow.__get_image_key(img_name)
                tk_img: PhotoImage = PhotoImage(img)

                self.__all_images[img_key] = img
                self.__all_images_tk[img_key] = tk_img

        # Dirts
        files: list[str] = VWSimulationWindow.__get_location_img_files(cast(str, self.__config["location_dirt_images_path"]))
        images_names: list[str] = [file.split(".")[0] for file in files]

        for name in images_names:
            file_path: str = os.path.join(cast(str, self.__config["location_dirt_images_path"]), name) + ".png"
            img: PILImage = VWSimulationWindow.__scale(Image.open(file_path), cast(int, self.__config["location_size"]))
            img_key: tuple[str, str] = VWSimulationWindow.__get_image_key(name)
            tk_img: PhotoImage = PhotoImage(img)

            self.__all_images[img_key] = img
            self.__all_images_tk[img_key] = tk_img

        self.__scaled_tk()

    @staticmethod
    def __construct_images(img: PILImage, name: str) -> OrderedDict[str, PILImage]:
        return OrderedDict({name + str(VWOrientation.north): img, name + str(VWOrientation.west): img.copy().rotate(90), name + str(VWOrientation.south): img.copy().rotate(180), name + str(VWOrientation.east): img.copy().rotate(270)})

    def __scaled_tk(self) -> None:
        size: int = int(min(cast(int, self.__config["location_size"]), cast(int, self.__config["grid_size"]) / self.__env.get_ambient().get_grid_dim()))

        for name, image in self.__all_images.items():
            self.__all_images_tk_scaled[name] = PhotoImage(VWSimulationWindow.__scale(image, size))

    @staticmethod
    def __scale(img: PILImage, lsize: int) -> PILImage:
        scale: float = lsize / max(img.width, img.height)

        return img.resize((int(img.width * scale), int(img.height * scale)), Resampling.BICUBIC)

    # Resize the grid.
    def __on_resize(self, value: int) -> None:
        value += cast(int, self.__config["min_environment_dim"])

        if value != self.__env.get_ambient().get_grid_dim():
            self.__env = VWEnvironment.generate_empty_env(config=self.__config, forced_line_dim=value)
            self.__init_dragables()
            self.__reset_canvas()
            self.__scaled_tk()
            self.__draw_grid()

    def __on_resize_slide(self, value: int) -> None:
        self.__size_text.set(str(value + cast(int, self.__config["min_environment_dim"])))

    def __on_leave_canvas(self, _: Any) -> None:
        self.__coordinate_text.set(self.__empty_location_coordinates_text)

    def __on_mouse_move(self, event: Event) -> None:
        if self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            env_dim: int = self.__env.get_ambient().get_grid_dim()
            size: int = cast(int, self.__config["grid_size"])
            inc: float = size / env_dim
            x: int = min(int(event.x // inc), env_dim - 1)
            y: int = min(int(event.y // inc), env_dim - 1)

            self.__coordinate_text.set(f"({x},{y})")
        else:
            self.__coordinate_text.set(self.__empty_location_coordinates_text)

    def __drag_on_start(self, event: Event) -> None:
        drag_manager, img_key = self.__dragables[cast(Canvas, event.widget).find_closest(event.x, event.y)[0]]

        drag_manager.set_drag_image(self.__all_images_tk_scaled[img_key])
        drag_manager.set_drag(self.__create_image(x=event.x, y=event.y, img=drag_manager.get_drag_image()))

        self.__canvas.itemconfigure(drag_manager.get_drag(), state="hidden")
        self.__canvas.tag_lower(drag_manager.get_drag())
        self.__selected = PyOptional.empty()

        # Keep the currently selected draggable on the top.
        for a in self.__canvas_agents.values():
            try:
                self.__canvas.tag_lower(a)
            except Exception:
                # If the draggable is not a valid argument for tag_lower, we ignore the error.
                pass

        for d in self.__canvas_dirts.values():
            try:
                self.__canvas.tag_lower(d)
            except Exception:
                # If the draggable is not a valid argument for tag_lower, we ignore the error.
                pass

    def __drag_on_drop(self, event: Event, drag_manager: VWCanvasDragManager) -> None:
        env_dim: int = self.__env.get_ambient().get_grid_dim()
        size: int = cast(int, self.__config["grid_size"])
        inc: float = size / env_dim
        x: int = min(int(event.x // inc), env_dim - 1)
        y: int = min(int(event.y // inc), env_dim - 1)
        coord: VWCoord = VWCoord(x=x, y=y)

        # Update the environment state.
        col, obj = drag_manager.get_key()
        colour: VWColour = VWColour(col)

        self.__drop_element(obj=obj, coord=coord, colour=colour, drag_manager=drag_manager)
        self.__select(event=event, print_message=False)
        self.redraw()

    def __drop_element(self, obj: str, coord: VWCoord, colour: VWColour, drag_manager: VWCanvasDragManager) -> None:
        if obj == "dirt":
            self.__drop_dirt(coord=coord, colour=colour, drag_manager=drag_manager)
        elif obj == "north":
            self.__drop_actor_facing_north(coord=coord, colour=colour, drag_manager=drag_manager)
        else:
            raise ValueError(f"Unknown obj: {obj}.")

    def __drop_dirt(self, coord: VWCoord, colour: VWColour, drag_manager:  VWCanvasDragManager) -> None:
        message: str = ""

        if self.__env.get_ambient().is_dirt_at(coord=coord):
            dirt_colour: VWColour = self.__env.get_ambient().get_location_interface(coord=coord).get_dirt_appearance().or_else_raise().get_colour()

            self.__env.remove_dirt(coord=coord)

            message += f" (replacing {dirt_colour.str_with_article()} dirt)"

        self.__env.drop_dirt(coord=coord, dirt_colour=colour)

        if coord in self.__canvas_dirts:
            self.__canvas.delete(self.__canvas_dirts[coord])

        self.__canvas_dirts[coord] = drag_manager.get_drag()
        self.__canvas.tag_lower(self.__canvas_dirts[coord])

        message = f"INFO: dropped {colour.str_with_article()} dirt at {coord}{message}"

        print(message)

    def __drop_actor_facing_north(self, coord: VWCoord, colour: VWColour, drag_manager: VWCanvasDragManager) -> None:
        message: str = ""

        actor, actor_appearance = VWActorsFactory.create_actor(colour=colour, orientation=VWOrientation.north, mind_surrogate=self.__agent_minds[colour])

        if self.__env.get_ambient().is_actor_at(coord=coord):
            actor_id: str = self.__env.get_ambient().get_location_interface(coord=coord).get_actor_appearance().or_else_raise().get_id()
            actor_colour: VWColour = self.__env.get_ambient().get_location_interface(coord=coord).get_actor_appearance().or_else_raise().get_colour()

            # Removes the actor appearance from the grid.
            self.__env.get_ambient().get_location_interface(coord=coord).remove_actor()
            # Removes the actor from the list of actors.
            self.__env.remove_actor(actor_id=actor_id)

            message += f" (replacing {actor_colour.str_with_article()} actor)"

        self.__env.add_actor(actor=actor)
        self.__env.get_ambient().get_location_interface(coord=coord).add_actor(actor_appearance=actor_appearance)
        self.__env.force_initial_perception_to_new_actor_after_stop(actor_id=actor_appearance.get_id())

        if coord in self.__canvas_agents:
            self.__canvas.delete(self.__canvas_agents[coord])

        self.__canvas_agents[coord] = drag_manager.get_drag()

        message = f"INFO: dropped {colour.str_with_article()} actor at {coord}{message}"

        print(message)

    def __show_hide_side(self, state: str) -> None:
        for item in self.__dragables.keys():
            self.__canvas.itemconfigure(item, state=state)

        if state == "hidden":
            self.__grid_scale_slider.pack_forget()
            self.__mid_frame.pack_forget()
            self.__info_frame.pack_forget()
        elif state == "normal":
            self.__grid_scale_slider.pack(side="bottom")
            self.__mid_frame.pack(side="left")
            self.__info_frame.pack(side="left", expand=True)

    def __get_selected_user_difficulty_level(self) -> int:
        assert isinstance(self.__buttons["difficulty"], VWDifficultyButton)

        return self.__buttons["difficulty"].get_difficulty()

    # Resets the grid and enviroment to the default values (empty 8x8).
    def __reset(self) -> None:
        print("INFO: reset")

        self.__env = VWEnvironment.generate_empty_env(config=self.__config)

        self.__grid_scale_slider.set_position(self.__env.get_ambient().get_grid_dim() - cast(int, self.__config["min_environment_dim"]))

        self.__init_dragables()
        self.__reset_canvas()
        self.__scaled_tk()
        self.__draw_grid()
        self.__reset_time_step()

    def play(self) -> None:
        '''
        Starts the proper simulation loop, and redraws the `Canvas` accordingly.
        '''
        self.__play()

    def __play(self) -> None:
        print("INFO: play")

        self.__pack_buttons("stop", "pause", "fast")
        self.__show_hide_side("hidden")
        self.__deselect()
        self.redraw()

        self.__running = True

        if self.__after_hook.is_present():  # Prevent button spam.
            self.__parent.after_cancel(self.__after_hook.or_else_raise())

        time: int = int(cast(float, self.__config["time_step"]) * 1000)

        self.__after_hook = PyOptional[str].of_nullable(self.__parent.after(time, self.__simulate))

    def __simulate(self) -> None:
        try:
            if self.__running:
                if self.__env.get_current_cycle_number() >= 0:
                    print(f"------------ Cycle {self.__env.get_current_cycle_number()} ------------ ")

                self.__env.evolve()
                self.__parent.after(0, self.redraw)

                time: int = int(cast(float, self.__config["time_step"]) * 1000)

                if self.__env.can_evolve():
                    self.__after_hook = PyOptional[str].of_nullable(self.__parent.after(time, self.__simulate))
                else:
                    self.__stop()
                    self.__reset()

                    raise VWEndOfCyclesException("INFO: end of cycles.")
        except VWEndOfCyclesException as e:
            print(e.args[0])

            self.__exit()
        except Exception:
            print("INFO: SIMULATION ERROR!")

            self.__running = False

            self.__error()

    def __stop(self) -> None:
        print("INFO: stop")

        self.__reset_time_step()
        self.__running = False
        self.__pack_buttons("play", "reset", "fast", "difficulty", "guide_bis", "save", "load")
        self.__show_hide_side("normal")

        for _, actor in self.__env.get_actors().items():
            actor.get_mind().reset_surrogate()

        self.redraw()

    def __resume(self) -> None:
        print("INFO: resume")

        self.__pack_buttons("stop", "pause", "fast")
        self.redraw()

        self.__running = True

        if self.__after_hook.is_present():  # Prevent button spam.
            self.__parent.after_cancel(self.__after_hook.or_else_raise())

        time = int(cast(float, self.__config["time_step"]) * 1000)
        self.__after_hook = PyOptional[str].of_nullable(self.__parent.after(time, self.__simulate))

    def __pause(self) -> None:
        print("INFO: pause")

        self.__reset_time_step()
        self.__pack_buttons("stop", "resume", "fast", "guide_bis")
        self.redraw()

        self.__running = False

    def __fast(self) -> None:
        self.__config["time_step_modifier"] = cast(float, self.__config["time_step_modifier"]) / 2
        self.__config["time_step"] = cast(float, self.__config["time_step_base"]) * self.__config["time_step_modifier"] + cast(float, self.__config["time_step_min"])

        VWSimulationWindow.__print_simulation_speed_message(time_step=self.__config["time_step"])

    def __reset_time_step(self) -> None:
        self.__config["time_step_modifier"] = 1.0
        self.__config["time_step"] = cast(float, self.__config["time_step_base"]) * self.__config["time_step_modifier"] + cast(float, self.__config["time_step_min"])

        VWSimulationWindow.__print_simulation_speed_message(time_step=self.__config["time_step"])

    def __difficulty(self) -> None:
        for actor_id, actor in self.__env.get_actors().items():
            difficulty_level: VWUserDifficulty = VWUserDifficulty(self.__get_selected_user_difficulty_level())

            if self.__env.get_actor_colour(actor_id=actor_id) == VWColour.user:
                assert isinstance(actor, VWUser)
                assert isinstance(actor.get_mind().get_surrogate(), VWUserMindSurrogate)

                actor.get_mind().get_surrogate().set_difficulty_level(difficulty_level=difficulty_level)

    @staticmethod
    def __print_simulation_speed_message(time_step: float) -> None:
        print(f"INFO: simulation speed set to {time_step:1.4f} s/cycle.")

    @staticmethod
    def __get_location_img_files(path: str) -> list[str]:
        return [file for file in os.listdir(path) if file.endswith(".png")]
