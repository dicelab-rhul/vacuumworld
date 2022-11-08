from tkinter import Event, Tk, Frame, Canvas, Label, StringVar, W, E, X, Image as Img
from typing import Callable, Dict, List, Tuple
from PIL import Image
from PIL.ImageTk import PhotoImage
from collections import OrderedDict

from ..autocomplete import AutocompleteEntry
from ..buttons.vwbutton import VWButton
from ..buttons.vwdifficultybutton import VWDifficultyButton
from ..slider import Slider
from ..drag_manager import CanvasDragManager
from ..bounds_manager import BoundsManager
from ...saveload import SaveStateManager

from ....common.coordinates import Coord
from ....common.orientation import Orientation
from ....common.direction import Direction
from ....common.colour import Colour
from ....common.exceptions import VWEndOfCyclesException
from ....model.actor.vwuser import VWUser
from ....model.actor.vwactor_appearance import VWActorAppearance
from ....model.actor.actor_mind_surrogate import ActorMindSurrogate
from ....model.actor.user_mind_surrogate import UserMindSurrogate
from ....model.actor.actor_factories import VWActorsFactory
from ....model.actor.user_difficulty import UserDifficulty
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
    def __init__(self, parent: Tk, config: dict, buttons: dict, minds: Dict[Colour, ActorMindSurrogate], env: VWEnvironment, _guide: Callable, _save: Callable, _load: Callable, _exit: Callable, _error: Callable) -> None:
        super(VWSimulationWindow, self).__init__(parent)

        self.__parent: Tk = parent
        self.__config: dict = config
        self.__bounds_manager: BoundsManager = BoundsManager(config=self.__config)
        self.__button_data: dict = buttons
        self.__env: VWEnvironment = env
        self.__guide: Callable = _guide
        self.__save: Callable = _save
        self.__load: Callable = _load
        self.__exit: Callable = _exit
        self.__error: Callable = _error
        self.__after_hook: Callable = None
        self.__save_state_manager: SaveStateManager = SaveStateManager()
        self.__empty_location_coordinates_text: str = "(-,-)"
        self.__load_menu: AutocompleteEntry = None
        self.__agent_minds: Dict[Colour, ActorMindSurrogate] = minds
        self.__running: bool = False
        self.__rectangle_selected: Img = None
        self.__selected: Coord = None
        self.__canvas_dirts: Dict[Coord, Img] = {}
        self.__canvas_agents: Dict[Coord, Img] = {}
        self.__all_images: Dict[Tuple[str, str], Img] = {}  # Will store all PIL images.
        self.__all_images_tk: Dict[Tuple[str, str], PhotoImage] = {}  # Will store all tk images.
        self.__all_images_tk_scaled: Dict[Tuple[str, str], PhotoImage] = {}  # Will store all tk images scaled to fit grid.
        self.__grid_lines: list = []  # Will store line objects.

        self.__create_and_display()

        # Note: pack() for VWSimulationWindow needs to be called by the caller.

    def __create_and_display(self) -> None:
        self.configure(background=self.__config["bg_colour"])

        self.__canvas: Canvas = Canvas(self, width=self.__config["grid_size"] + self.__config["location_size"] + 4, height=self.__config["grid_size"] + 1, bd=0, highlightthickness=0)

        self.__init_buttons()

        self.__canvas.configure(background=self.__config["bg_colour"])

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

    def __load_button_image(self, button_name: str) -> Img:
        return VWSimulationWindow.__scale(Image.open(os.path.join(self.__config["button_data_path"], self.__button_data[button_name]["image_file"])), self.__config["button_size"])

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
        action: Callable = self.__button_data[button_name]["action"]
        image: Img = self.__load_button_image(button_name=button_name)
        tip_text: str = self.__button_data[button_name]["tip_text"]

        return VWButton(parent=parent, config=self.__config, img=image, fun=action, text=None, tip_text=tip_text)

    def __build_difficulty_button(self, parent: Frame) -> VWDifficultyButton:
        image: Img = self.__load_button_image(button_name="difficulty")
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
        files: List[str] = self.__save_state_manager.get_ordered_list_of_filenames_in_save_directory()
        self.__load_menu: AutocompleteEntry = AutocompleteEntry(files, 3, self.__mid_frame, font=self.__config["root_font"], bg=self.__config["autocomplete_entry_bg_colour"], fg=self.__config["fg_colour"])
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
        size_label: Label = Label(_size_frame, textvariable=self.__size_text, width=2, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        size_label.grid(row=0, column=1, sticky=E)

        _size: StringVar = StringVar()
        _size.set("size:")
        _size_label: Label = Label(_size_frame, textvariable=_size, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        _size_label.grid(row=0, column=0, sticky=W)
        _size_frame.grid(row=0, column=0, stick=W)

        self.__coordinate_text: StringVar = StringVar()
        self.__coordinate_text.set(self.__empty_location_coordinates_text)
        coordinate_label: Label = Label(self.__info_frame, textvariable=self.__coordinate_text, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        coordinate_label.grid(row=1, column=0, sticky=W)

        self.__info_frame.pack(side="left", expand=True)
        self.__button_frame.grid(row=1, column=0, pady=3, sticky=W+E)

    def __init_buttons(self) -> None:
        self.__buttons: Dict[str, VWButton] = {}

        self.__set_button_actions()

        bg: str = self.__config["bg_colour"]

        self.__button_frame: Frame = Frame(self, bg=bg)

        self.__init_bottom_left_frame(bg=bg)
        self.__init_saveload_frame(bg=bg)
        self.__init_info_frame(bg=bg)

    def __init_size_slider(self, parent, length=250) -> None:
        increments: int = self.__config["max_environment_dim"] - self.__config["min_environment_dim"]
        self.__grid_scale_slider: Slider = Slider(parent, self.__config, self.__on_resize, self.__on_resize_slide, length * self.__config["scale"], 16 * self.__config["scale"], slider_width=length * self.__config["scale"]/(increments * 3), increments=increments, start=self.__config["grid_size"]/self.__config["location_size"] - self.__config["min_environment_dim"])

        self.__grid_scale_slider.pack(side="top")

    def __init_dragables(self) -> None:
        # Load all images.
        keys: List[Tuple[str, str]] = [("white", "north"), ("orange", "north"), ("green", "north"), ("user", "north"), ("orange", "dirt"), ("green", "dirt")]

        self.__dragables: Dict[Img, Tuple[CanvasDragManager, Tuple[str, str]]] = {}

        ix: int = self.__config["grid_size"] + self.__config["location_size"] / 2 + 2
        iy: int = self.__config["location_size"] / 2 + 4

        for i, key in enumerate(keys):
            item: Img = self.__canvas.create_image(ix, iy + i * self.__config["location_size"], image=self.__all_images_tk[key])
            drag_manager: CanvasDragManager = CanvasDragManager(self.__config, key, self.__env.get_ambient().get_grid_dim(), self.__canvas, item, self.__drag_on_start, self.__drag_on_drop)
            self.__dragables[item] = (drag_manager, key)

    def __deselect(self) -> None:
        self.__selected = None
        if self.__rectangle_selected:
            self.__canvas.delete(self.__rectangle_selected)
        self.__rectangle_selected = None

    def __select(self, event: Event, print_message: bool=True) -> None:
        if not self.__running and self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            self.__deselect()
            self.focus()
            inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()
            coordinate: Coord = Coord(x=int(event.x / inc), y=int(event.y / inc))

            if print_message:
                print("SELECT: selected location {}.".format(coordinate))

            self.__selected = coordinate
            xx: int = coordinate.get_x() * inc
            yy: int = coordinate.get_y() * inc
            self.__rectangle_selected = self.__canvas.create_rectangle((xx, yy, xx + inc, yy + inc), fill="", width=3)

    def __remove_top(self, event: Event) -> None:
        if not self.__running and self.__bounds_manager.in_bounds(x=event.x, y=event.y):

            print("remove top")

            inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()
            coordinate: Coord = Coord(x=int(event.x / inc), y=int(event.y / inc))

            if coordinate in self.__env.get_ambient().get_grid():
                location: VWLocation = self.__env.get_ambient().get_location_interface(coord=coordinate)

                if location.has_actor():
                    actor_id: str = location.get_actor_appearance().get_id()
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
    def __remove_dirt_from_gui(self, coordinate: Coord) -> None:
        old: Img = self.__canvas_dirts[coordinate]
        self.__canvas.delete(old)
        del old

    # Remove an agent from the view of the grid.
    def __remove_actor_from_gui(self, coordinate: Coord) -> None:
        old: Img = self.__canvas_agents[coordinate]
        self.__canvas.delete(old)
        del old

    def __rotate_actor(self, _, direction: Direction) -> None:
        if not self.__selected:
            return

        working_location: VWLocation = self.__env.get_ambient().get_location_interface(coord=self.__selected)

        if working_location and working_location.has_actor():
            self.__remove_actor_from_gui(self.__selected)

            new_orientation: Orientation = working_location.get_actor_appearance().get_orientation().get(direction=direction)
            actor_colour: Colour = working_location.get_actor_appearance().get_colour()
            inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()
            tk_img: PhotoImage = self.__all_images_tk_scaled[(actor_colour.value, new_orientation.value)]
            item: Img = self.__canvas.create_image(self.__selected.get_x() * inc + inc/2, self.__selected.get_y() * inc + inc/2, image=tk_img)
            self.__canvas_agents[self.__selected] = item

            self.__env.turn_actor(coord=self.__selected, direction=direction)
            self.__lines_to_front()

    def __rotate_actor_left(self, event: Event) -> None:
        self.__rotate_actor(event, Direction.left)

    def __rotate_actor_right(self, event:  Event) -> None:
        self.__rotate_actor(event, Direction.right)

    def __pack_buttons(self, *buttons, forget: bool=True) -> None:
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
        if self.__rectangle_selected:
            self.__canvas.tag_raise(self.__rectangle_selected)

    def __load_and_redraw(self, load_menu) -> None:
        try:
            loaded_env: VWEnvironment = self.__load(load_menu)
        except Exception:
            if self.__config["file_to_load"] not in (None, ""):
                print("Something went wrong. Could not load any grid from {}".format(self.__config["file_to_load"]))
            else:
                print("Something went wrong. Could not load any grid.")

            loaded_env: VWEnvironment = VWEnvironment.generate_empty_env(config=self.__config)
        finally:
            self.__redraw_loaded_env(loaded_env=loaded_env)

    def __redraw_loaded_env(self, loaded_env: VWEnvironment) -> None:
        if loaded_env is not None:
            self.__env = loaded_env
            self.__grid_scale_slider.set_position(self.__env.get_ambient().get_grid_dim() - self.__config["min_environment_dim"])
            self.__reset_canvas()
            self.__scaled_tk()
            self.__draw_grid()
            self.redraw()

    def redraw(self) -> None:
        '''
        This method resets and redraws the `Canvas` according to the wrapped `VWEnvironment`.
        '''
        self.__reset_canvas(lines=False)

        inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()

        for coord, location in self.__env.get_ambient().get_grid().items():
            if location:
                self.__redraw_location(coord=coord, location=location, inc=inc)

    def __redraw_location(self, coord: Coord, location: VWLocation, inc: int) -> None:
        assert location

        if location.has_actor():
            actor_appearance: VWActorAppearance = location.get_actor_appearance()
            tk_img: PhotoImage = self.__all_images_tk_scaled[(actor_appearance.get_colour().value, actor_appearance.get_orientation().value)]
            item: Img = self.__canvas.create_image(coord.get_x() * inc + inc/2, coord.get_y() * inc + inc/2, image=tk_img)

            self.__canvas_agents[coord] = item

            self.__canvas.tag_lower(item)  # Keep the agent behind the grid lines.

            if coord in self.__canvas_dirts:  # Keep the dirt behind the agent.
                self.__canvas.tag_lower(self.__canvas_dirts[coord])

        if location.has_dirt():
            tk_img: PhotoImage = self.__all_images_tk_scaled[(location.get_dirt_appearance().get_colour().value, "dirt")]
            item: Img = self.__canvas.create_image(coord.get_x() * inc + inc/2, coord.get_y() * inc + inc/2, image=tk_img)

            self.__canvas_dirts[coord] = item

            self.__canvas.tag_lower(item)  # Keep dirt behind agents and grid lines.

    def __draw_grid(self) -> None:
        env_dim: int = self.__env.get_ambient().get_grid_dim()
        size: int = self.__config["grid_size"]

        x: int = 0
        y: int = 0
        inc: int = size / env_dim

        for _ in range(env_dim + 1):
            self.__grid_lines.append(self.__canvas.create_line(x, 0, x, size+1))
            self.__grid_lines.append(self.__canvas.create_line(0, y, size+1, y))

            y += inc
            x += inc

    @staticmethod
    def __get_image_key(name: str) -> Tuple[str, str]:
        s = name.split("_")

        return (s[0], s[1])

    def __init_images(self) -> None:
        # Agents
        files: List[str] = VWSimulationWindow.__get_location_img_files(self.__config["location_agent_images_path"])
        image_names: List[str] = [file.split(".")[0] for file in files]

        for img_name in image_names:
            file_path: str = os.path.join(self.__config["location_agent_images_path"], img_name) + ".png"
            img: Img = VWSimulationWindow.__scale(Image.open(file_path), self.__config["location_size"])
            images: OrderedDict[str, Img] = VWSimulationWindow.__construct_images(img, img_name + "_")

            for img_name, img in images.items():
                img_key: Tuple[str, str] = VWSimulationWindow.__get_image_key(img_name)
                tk_img: PhotoImage = PhotoImage(img)

                self.__all_images[img_key] = img
                self.__all_images_tk[img_key] = tk_img

        # Dirts
        files: List[str] = VWSimulationWindow.__get_location_img_files(self.__config["location_dirt_images_path"])
        images_names: List[str] = [file.split(".")[0] for file in files]

        for name in images_names:
            file_path: str = os.path.join(self.__config["location_dirt_images_path"], name) + ".png"
            img: Img = VWSimulationWindow.__scale(Image.open(file_path), self.__config["location_size"])
            img_key: Tuple[str, str] = VWSimulationWindow.__get_image_key(name)
            tk_img: PhotoImage = PhotoImage(img)

            self.__all_images[img_key] = img
            self.__all_images_tk[img_key] = tk_img

        self.__scaled_tk()

    @staticmethod
    def __construct_images(img: Img, name: str) -> Dict[str, Img]:
        return OrderedDict({name + str(Orientation.north): img, name + str(Orientation.west): img.copy().rotate(90), name + str(Orientation.south): img.copy().rotate(180), name + str(Orientation.east): img.copy().rotate(270)})

    def __scaled_tk(self) -> None:
        size: int = min(self.__config["location_size"], self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim())
        for name, image in self.__all_images.items():
            self.__all_images_tk_scaled[name] = PhotoImage(VWSimulationWindow.__scale(image, size))

    @staticmethod
    def __scale(img: Img, lsize: int) -> Img:
        scale: int = lsize / max(img.width, img.height)
        return img.resize((int(img.width * scale), int(img.height * scale)), Image.BICUBIC)

    # Resize the grid.
    def __on_resize(self, value: int) -> None:
        value += self.__config["min_environment_dim"]

        if value != self.__env.get_ambient().get_grid_dim():
            self.__env = VWEnvironment.generate_empty_env(config=self.__config, forced_line_dim=value)
            self.__init_dragables()
            self.__reset_canvas()
            self.__scaled_tk()
            self.__draw_grid()

    def __on_resize_slide(self, value: int) -> None:
        self.__size_text.set(str(value + self.__config["min_environment_dim"]))

    def __on_leave_canvas(self, _) -> None:
        self.__coordinate_text.set(self.__empty_location_coordinates_text)

    def __on_mouse_move(self, event: Event) -> None:
        if self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()

            self.__coordinate_text.set("({},{})".format(int(event.x / inc), int(event.y / inc)))
        else:
            self.__coordinate_text.set(self.__empty_location_coordinates_text)

    def __drag_on_start(self, event: Event) -> None:
        drag_manager, img_key = self.__dragables[event.widget.find_closest(event.x, event.y)[0]]

        drag_manager.set_drag_image(self.__all_images_tk_scaled[img_key])
        drag_manager.set_drag(self.__canvas.create_image(event.x, event.y, image=drag_manager.get_drag_image()))

        self.__canvas.itemconfigure(drag_manager.get_drag(), state="hidden")
        self.__canvas.tag_lower(drag_manager.get_drag())
        self.__selected = None

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

    def __drag_on_drop(self, event: Event, drag_manager: CanvasDragManager) -> None:
        inc: int = self.__config["grid_size"] / self.__env.get_ambient().get_grid_dim()
        x: int = int(event.x / inc)
        y: int = int(event.y / inc)
        coord: Coord = Coord(x=x, y=y)

        # Update the environment state.
        col, obj = drag_manager.get_key()
        colour: Colour = Colour(col)

        self.__drop_element(obj=obj, coord=coord, colour=colour, drag_manager=drag_manager)
        self.__select(event=event, print_message=False)
        self.redraw()

    def __drop_element(self, obj: str, coord: Coord, colour: Colour, drag_manager: CanvasDragManager) -> None:
        if obj == "dirt":
            self.__drop_dirt(coord=coord, colour=colour, drag_manager=drag_manager)
        elif obj == "north":
            self.__drop_actor_facing_north(coord=coord, colour=colour, drag_manager=drag_manager)
        else:
            raise ValueError("Unknown obj: {}.".format(obj))

    def __drop_dirt(self, coord: Coord, colour: Colour, drag_manager:  CanvasDragManager) -> None:
        message: str = ""

        if self.__env.get_ambient().is_dirt_at(coord=coord):
            dirt_colour: Colour = self.__env.get_ambient().get_location_interface(coord=coord).get_dirt_appearance().get_colour()

            self.__env.remove_dirt(coord=coord)

            message += " (replacing {} dirt)".format(dirt_colour.str_with_article())

        self.__env.drop_dirt(coord=coord, dirt_colour=colour)

        if coord in self.__canvas_dirts:
            self.__canvas.delete(self.__canvas_dirts[coord])

        self.__canvas_dirts[coord] = drag_manager.get_drag()
        self.__canvas.tag_lower(self.__canvas_dirts[coord])

        message = "INFO: dropped {} dirt at {}".format(colour.str_with_article(), coord) + message

        print(message)

    def __drop_actor_facing_north(self, coord: Coord, colour: Colour, drag_manager: CanvasDragManager) -> None:
        message: str = ""

        actor, actor_appearance = VWActorsFactory.create_actor(colour=colour, orientation=Orientation.north, mind_surrogate=self.__agent_minds[colour])

        if self.__env.get_ambient().is_actor_at(coord=coord):
            actor_id: str = self.__env.get_ambient().get_location_interface(coord=coord).get_actor_appearance().get_id()
            actor_colour: Colour = self.__env.get_ambient().get_location_interface(coord=coord).get_actor_appearance().get_colour()

            # Removes the actor appearance from the grid.
            self.__env.get_ambient().get_location_interface(coord=coord).remove_actor()
            # Removes the actor from the list of actors.
            self.__env.remove_actor(actor_id=actor_id)

            message += " (replacing {} actor)".format(actor_colour.str_with_article())

        self.__env.add_actor(actor=actor)
        self.__env.get_ambient().get_location_interface(coord=coord).add_actor(actor_appearance=actor_appearance)

        if coord in self.__canvas_agents:
            self.__canvas.delete(self.__canvas_agents[coord])

        self.__canvas_agents[coord] = drag_manager.get_drag()

        message = "INFO: dropped {} actor at {}".format(colour.str_with_article(), coord) + message

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

        self.__grid_scale_slider.set_position(self.__env.get_ambient().get_grid_dim() - self.__config["min_environment_dim"])

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

        if self.__after_hook:  # Prevent button spam.
            self.__parent.after_cancel(self.__after_hook)

        time: int = int(self.__config["time_step"]*1000)
        self.__after_hook = self.__parent.after(time, self.__simulate)

    def __simulate(self) -> None:
        try:
            if self.__running:
                if self.__env.get_current_cycle_number() >= 0:
                    print("------------ Cycle {} ------------ ".format(self.__env.get_current_cycle_number()))

                self.__env.evolve()
                self.__parent.after(0, self.redraw)

                time: int = int(self.__config["time_step"]*1000)

                if self.__env.can_evolve():
                    self.__after_hook = self.__parent.after(time, self.__simulate)
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

        if self.__after_hook:  # Prevent button spam.
            self.__parent.after_cancel(self.__after_hook)

        time = int(self.__config["time_step"]*1000)
        self.__after_hook = self.__parent.after(time, self.__simulate)

    def __pause(self) -> None:
        print("INFO: pause")

        self.__reset_time_step()
        self.__pack_buttons("stop", "resume", "fast", "guide_bis")
        self.redraw()

        self.__running = False

    def __fast(self) -> None:
        self.__config["time_step_modifier"] /= 2.
        self.__config["time_step"] = self.__config["time_step_base"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

        VWSimulationWindow.__print_simulation_speed_message(time_step=self.__config["time_step"])

    def __reset_time_step(self) -> None:
        self.__config["time_step_modifier"] = 1.
        self.__config["time_step"] = self.__config["time_step_base"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

        VWSimulationWindow.__print_simulation_speed_message(time_step=self.__config["time_step"])

    def __difficulty(self) -> None:
        for actor_id, actor in self.__env.get_actors().items():
            difficulty_level: UserDifficulty = UserDifficulty(self.__get_selected_user_difficulty_level())

            if self.__env.get_actor_colour(actor_id=actor_id) == Colour.user:
                assert isinstance(actor, VWUser)
                assert isinstance(actor.get_mind().get_surrogate(), UserMindSurrogate)

                actor.get_mind().get_surrogate().set_difficulty_level(difficulty_level=difficulty_level)

    @staticmethod
    def __print_simulation_speed_message(time_step: float) -> None:
        print("INFO: simulation speed set to {:1.4f} s/cycle".format(time_step))

    @staticmethod
    def __get_location_img_files(path: str) -> List[str]:
        return [file for file in os.listdir(path) if file.endswith(".png")]
