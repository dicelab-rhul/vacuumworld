from tkinter import Tk, Frame, Canvas, Label, StringVar, W, E, X
from typing import Callable
from vacuumworld.utils.saveload import SaveStateManager
from PIL import ImageTk, Image
from collections import OrderedDict

from ..buttons.vwbutton import VWButton
from ..buttons.vwdifficultybutton import VWDifficultyButton
from ..slider import Slider
from ..drag_manager import CanvasDragManager
from ....core.environment.vw import Grid
from ....core.environment.vwenvironment import init as init_environment
from ....core.common.coordinates import Coord
from ....core.common.direction import Direction
from ....core.common.orientation import Orientation
from ....utils.vwutils import get_location_img_files, print_simulation_speed_message
from ....utils.autocomplete import AutocompleteEntry

import os



#TODO: check and remove the unnecessary stuff.
class VWSimulationWindow(Frame):
    def __init__(self, root: Tk, config: dict, minds: list, user_mind: int, grid: Grid, _guide: Callable, _save: Callable, _load: Callable, _finish: Callable, _error: Callable) -> None:
        super(VWSimulationWindow, self).__init__(root)

        self.__root: Tk = root
        self.__drag_manager: CanvasDragManager = None
        self.__config: dict = config
        self.__grid: Grid = grid
        self.__guide: Callable = _guide
        self.__save: Callable = _save
        self.__load: Callable = _load
        self.__finish: Callable = _finish
        self.__error: Callable = _error
        self.after_hook: Callable = None
        self.__save_state_manager: SaveStateManager = SaveStateManager()
        self.__empty_location_coordinates_text: str = "(-,-)"


        self.configure(background=self.__config["bg_colour"])
        self.canvas: Canvas = Canvas(self, width=self.__config["grid_size"]+self.__config["location_size"]+4, height=self.__config["grid_size"]+1, bd=0,highlightthickness=0)

        self._init_buttons()

        self.canvas.configure(background=self.__config["bg_colour"])

        self.canvas_dirts = {}
        self.canvas_agents = {}

        self.all_images = {} #stores all PIL images
        self.all_images_tk = {} #stores all tk images
        self.all_images_tk_scaled = {} #stores all tk images scale to fit grid
        self.grid_lines = [] #stores line objects

        self.env = None
        self.reset: bool = False
        self.current_user_mind = user_mind
        self.agent_minds: list = minds

        self._init_images()
        self._init_dragables()

        self._draw_grid()

        self.canvas.grid(row=0,column=0) #packing

        #bind keys for rotation
        self.__root.bind("<Left>", self.rotate_agent_left)
        self.__root.bind("<Right>", self.rotate_agent_right)
        self.__root.bind("<a>", self.rotate_agent_left)
        self.__root.bind("<d>", self.rotate_agent_right)

        self.canvas.bind("<Double-Button-1>", self.remove_top)
        self.canvas.bind("<Button-1>", self.select)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_leave_canvas)
        
        
        self.currently_selected = None
        self.running = False
        self.rectangle_selected = None
        self.selected = None

        # Note: pack() needs to be called by the caller.

    def _init_buttons(self):
        self.buttons = {}

        bg = self.__config["bg_colour"]
        buttons = get_location_img_files(self.__config["button_images_path"])
        buttons = {b.split(".")[0]:b for b in buttons}

        self.button_frame = Frame(self, bg=bg)

        
        play_img = VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["play"])), self.__config["button_size"])

        #left side contains buttons and slider
        self.left_frame = Frame(self.button_frame, bg=bg)
        self.slider_frame = Frame(self.left_frame, bg=bg)
        self.control_buttons_frame = Frame(self.left_frame, bg=bg)
        
        self.buttons["play"] = VWButton(self.control_buttons_frame, self.__config, play_img , self._play, tip_text="Click here to start the simulation.")
        self.buttons["resume"] = VWButton(self.control_buttons_frame, self.__config, play_img, self._resume, tip_text="Click here to resume the simulation.")
        self.buttons["pause"] = VWButton(self.control_buttons_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["pause"])), self.__config["button_size"]), self._pause, tooltip=self.__config["tooltips"], tip_text="Click here to pause the simulation.")
        self.buttons["stop"] = VWButton(self.control_buttons_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["stop"])), self.__config["button_size"]), self._stop, tooltip=self.__config["tooltips"], tip_text="Click here to stop the simulation.")
        self.buttons["fast"] = VWButton(self.control_buttons_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["fast"])), self.__config["button_size"]), self._fast, tooltip=self.__config["tooltips"], tip_text= "Click here to fast-forward the simulation.")
        self.buttons["reset"] = VWButton(self.control_buttons_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["reset"])), self.__config["button_size"]), self._reset, tooltip=self.__config["tooltips"], tip_text="Click here to reset the grid.")
        self.buttons["guide"] = VWButton(self.control_buttons_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["guide"])), self.__config["button_size"]), self.__guide, tooltip=self.__config["tooltips"], tip_text="Click here to open the project's GitHub page.")
        
        dif_img = VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["difficulty"])), self.__config["button_size"])
        self.buttons["difficulty"] = VWDifficultyButton(self.control_buttons_frame, self.__config, dif_img, self._difficulty, tip_text="Click here to toggle the user difficulty level.")
        
        self.pack_buttons("play", "reset", "fast", "difficulty", "guide", forget=False)
        
        #init the slider
        self._init_size_slider(self.slider_frame)
        
        self.slider_frame.grid(row=0, column=0)
        self.control_buttons_frame.grid(row=1, column=0, sticky=W)

        self.left_frame.pack(side="left", fill=X)
  
        #middle contains save and load
        self.mid_frame = Frame(self.button_frame, bg=bg)
        self.saveload_frame = Frame(self.mid_frame, bg=bg)
    
        #buttons
        self.buttons["save"] = VWButton(self.saveload_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["save"])), self.__config["button_size"]), lambda: self.__save(self.load_menu), tooltip=self.__config["tooltips"], tip_text="Click here to save the current state.")
        self.buttons["load"] = VWButton(self.saveload_frame, self.__config, VWSimulationWindow._scale(Image.open(os.path.join(self.__config["button_images_path"], buttons["load"])), self.__config["button_size"]), lambda: self.__load_and_redraw(self.load_menu), tooltip=self.__config["tooltips"], tip_text="Click here to load a savestate.")
        
        #entry box
        files = self.__save_state_manager.get_ordered_list_of_filenames_in_save_directory()
        self.load_menu = AutocompleteEntry(files, 3, self.mid_frame, font=self.__config["root_font"], bg=self.__config["autocomplete_entry_bg_colour"], fg=self.__config["fg_colour"])
        self.load_menu.bind("<Button-1>", lambda _: self.deselect())
        self.load_menu.pack(side="top")
    
        self.pack_buttons("save", "load", forget=False)
        self.saveload_frame.pack(side="bottom")
        self.mid_frame.pack(side="left")

        #init information frame
        self.info_frame = Frame(self.button_frame, bg=bg)
        
        _size_frame = Frame(self.info_frame, bg=bg)
        self.size_text = StringVar()
        self.size_text.set(str(self.__config["initial_environment_dim"]))
        self.size_label = Label(_size_frame, textvariable=self.size_text, width=2, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        self.size_label.grid(row=0, column=1, sticky=E)
        
        _size = StringVar()
        _size.set("size:")
        _size_label =  Label(_size_frame, textvariable=_size, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        _size_label.grid(row=0, column=0, sticky=W)
        _size_frame.grid(row=0, column=0, stick=W)
        
        self.coordinate_text = StringVar()
        self.coordinate_text.set(self.__empty_location_coordinates_text)
        self.coordinate_label = Label(self.info_frame, textvariable=self.coordinate_text, font=self.__config["root_font"], bg=bg, fg=self.__config["fg_colour"])
        self.coordinate_label.grid(row=1, column=0, sticky=W)

        self.info_frame.pack(side="left", expand=True)
        self.button_frame.grid(row=1, column=0, pady=3, sticky=W+E)

        return buttons
    
    def _init_size_slider(self, parent, length=250):
        increments = Grid.GRID_MAX_SIZE - Grid.GRID_MIN_SIZE
        self.grid_scale_slider = Slider(parent, self.__config, self.on_resize, self.on_resize_slide, length * self.__config["scale"],
                                        16 * self.__config["scale"], slider_width = length * self.__config["scale"] / (increments * 3),
                                        increments=increments,
                                        start=self.__config["grid_size"]/self.__config["location_size"] - Grid.GRID_MIN_SIZE)
        self.grid_scale_slider.pack(side="top")
        
    def _init_dragables(self):
        #load all images
        keys = [("white", "north"), 
                ("orange", "north"), 
                ("green", "north"), 
                ("user", "north"), 
                ("orange", "dirt"), 
                ("green", "dirt")]
        self.dragables = {}

        ix = self.__config["grid_size"] + self.__config["location_size"] / 2 + 2
        iy = self.__config["location_size"] / 2 + 4

        for i, key in enumerate(keys):
            item = self.canvas.create_image(ix, iy + i * self.__config["location_size"], image=self.all_images_tk[key])
            self.__drag_manager = CanvasDragManager(self.__config, key, self.__grid, self.canvas, item, self.drag_on_start, self.drag_on_drop)
            self.dragables[item] = (self.__drag_manager, key)

    def deselect(self):
        self.selected = None
        if self.rectangle_selected:
            self.canvas.delete(self.rectangle_selected)
        self.rectangle_selected = None

    def select(self, event):
        if not self.running and self.__drag_manager.in_bounds(event.x, event.y):
            self.deselect()
            self.focus()
            inc = self.__config["grid_size"] / self.__grid.dim
            coordinate = Coord(int(event.x / inc), int(event.y / inc))
            print("SELECT:", self.__grid.state[coordinate])
            self.selected = self.__grid.state[coordinate]
            xx = coordinate.x * inc
            yy = coordinate.y * inc
            self.rectangle_selected = self.canvas.create_rectangle((xx, yy, xx + inc, yy + inc), fill="", width=3)


    def remove_top(self, event):
        if not self.running and self.__drag_manager.in_bounds(event.x, event.y):
            print("remove top")
            inc = self.__config["grid_size"] / self.__grid.dim
            coordinate = Coord(int(event.x / inc), int(event.y / inc))
            location = self.__grid.state[coordinate]
            if location.agent:
                self.remove_agent(coordinate)
                self.__grid.remove_agent(coordinate)
            elif self.__grid.state[coordinate].dirt:
                self.remove_dirt(coordinate)
                self.__grid.remove_dirt(coordinate)

    #remove an agent from the view
    def remove_dirt(self, coordinate):
        old = self.canvas_dirts[coordinate]
        self.canvas.delete(old)
        del old

    #remove an agent from the view
    def remove_agent(self, coordinate):
        old = self.canvas_agents[coordinate]
        self.canvas.delete(old)
        del old

    def rotate_agent(self, _, direction):
        if self.selected and self.selected.agent:
            print(self.selected)
            self.remove_agent(self.selected.coordinate)
            new_orientation =  direction(self.selected.agent.orientation).value
            inc = self.__config["grid_size"] / self.__grid.dim
            tk_img = self.all_images_tk_scaled[(self.selected.agent.colour.value, new_orientation)]
            item = self.canvas.create_image(self.selected.coordinate.x * inc + inc/2,
                                            self.selected.coordinate.y * inc + inc/2, image=tk_img)
            self.canvas_agents[self.selected.coordinate] = item
            self.__grid.turn_agent(self.selected.coordinate, new_orientation)
            self.selected = self.__grid.state[self.selected.coordinate]
            self._lines_to_front()

    def rotate_agent_left(self, event):
        self.rotate_agent(event, Direction.left)

    def rotate_agent_right(self, event):
        self.rotate_agent(event, Direction.right)

    def pack_buttons(self, *buttons, forget=True):
        if forget:
            for button in self.buttons.values():
               button.get_button().grid_remove()
        for i in range(len(buttons)):
            self.buttons[buttons[i]].get_button().grid(row=0, column=i, sticky=W)

    def _reset_canvas(self, lines=True, dirts=True, agents=True, select=True):
        if lines:
            for line in self.grid_lines:
                self.canvas.delete(line)
            self.grid_lines.clear()
        if agents:
            for a in self.canvas_agents.values():
                self.canvas.delete(a)
            self.canvas_agents.clear()
        if dirts:
            for d in self.canvas_dirts.values():
                self.canvas.delete(d)
            self.canvas_dirts.clear()
        if select:
            self.deselect()

    def _lines_to_front(self):
        for line in self.grid_lines:
            self.canvas.tag_raise(line)
        if self.rectangle_selected:
            self.canvas.tag_raise(self.rectangle_selected)

    def _reset_canvas_agents(self):
        for a in self.canvas_agents.values():
            self.canvas.delete(a)
        self.canvas_agents.clear()

    def __load_and_redraw(self, load_menu) -> None:
        loaded_grid: Grid = self.__load(load_menu)

        if loaded_grid is not None:
            self.__grid = loaded_grid
            self.grid_scale_slider.set_position(self.__grid.dim - Grid.GRID_MIN_SIZE)
            self._reset_canvas()
            self._scaled_tk()
            self._draw_grid()
            self._redraw()

    def _redraw(self):
        self._reset_canvas(lines=False)
        inc = self.__config["grid_size"] / self.__grid.dim
        for coord, location in self.__grid.state.items():
            if location:
                if location.agent:
                    tk_img = self.all_images_tk_scaled[(location.agent.colour.value, location.agent.orientation.value)]
                    item = self.canvas.create_image(coord.x * inc + inc/2,
                                                    coord.y * inc + inc/2, image=tk_img)
                    self.canvas_agents[coord] = item
                    self.canvas.tag_lower(item) #keep the agent behind the grid lines
                    if coord in self.canvas_dirts: #keep the dirt behind the agent
                        self.canvas.tag_lower(self.canvas_dirts[coord])
                if location.dirt:
                    tk_img = self.all_images_tk_scaled[(location.dirt.colour.value, "dirt")]
                    item = self.canvas.create_image(coord.x * inc + inc/2, coord.y * inc + inc/2, image=tk_img)
                    self.canvas_dirts[coord] = item
                    self.canvas.tag_lower(item) #keep dirt behind agents and grid lines

    def _draw_grid(self):
        env_dim: int = self.__grid.dim
        size: int = self.__config["grid_size"]

        x = 0
        y = 0
        inc = size / env_dim
        for _ in range(env_dim + 1):
           self.grid_lines.append(self.canvas.create_line(x,0,x,size+1))
           self.grid_lines.append(self.canvas.create_line(0,y,size+1,y))
           y += inc
           x += inc

    @staticmethod
    def _get_image_key(name):
        s = name.split("_")
        return (s[0], s[1])

    def _init_images(self):
        # agents
        files = get_location_img_files(self.__config["location_agent_images_path"])
        image_names = [file.split(".")[0] for file in files]

        for img_name in image_names:
            file = os.path.join(self.__config["location_agent_images_path"], img_name) +  ".png"
            img = VWSimulationWindow._scale(Image.open(file), self.__config["location_size"])
            images = VWSimulationWindow._construct_images(img, img_name + "_")
            for img_name, img in images.items():
                img_key = VWSimulationWindow._get_image_key(img_name)
                tk_img = ImageTk.PhotoImage(img)
                self.all_images[img_key] = img
                self.all_images_tk[img_key] = tk_img

        # dirts
        files = get_location_img_files(self.__config["location_dirt_images_path"])
        images_names = [file.split(".")[0] for file in files]

        for name in images_names:
            file = os.path.join(self.__config["location_dirt_images_path"], name) +  ".png"
            img = VWSimulationWindow._scale(Image.open(file), self.__config["location_size"])
            img_key = VWSimulationWindow._get_image_key(name)
            tk_img = ImageTk.PhotoImage(img)
            self.all_images[img_key] = img
            self.all_images_tk[img_key] = tk_img

        self._scaled_tk()

    @staticmethod
    def _construct_images(img, name):
        return OrderedDict({name + str(Orientation.north):img,
                      name + str(Orientation.west):img.copy().rotate(90),
                      name + str(Orientation.south):img.copy().rotate(180),
                      name + str(Orientation.east):img.copy().rotate(270)})

    def _scaled_tk(self):
        size = min(self.__config["location_size"], self.__config["grid_size"]  / self.__grid.dim)
        for name, image in self.all_images.items():
            self.all_images_tk_scaled[name] = ImageTk.PhotoImage(VWSimulationWindow._scale(image, size))

    @staticmethod
    def _scale(img, lsize):
        scale = lsize / max(img.width, img.height)
        return img.resize((int(img.width * scale), int(img.height * scale)), Image.BICUBIC)

    #resize the grid
    def on_resize(self, value):
        value =  value + Grid.GRID_MIN_SIZE
        if value != self.__grid.dim:
            self.__grid.reset(value)
            self._reset_canvas()
            self._scaled_tk()
            self._draw_grid()
            
    def on_resize_slide(self, value):
        self.size_text.set(str(value + Grid.GRID_MIN_SIZE))

    def on_leave_canvas(self, _):
        self.coordinate_text.set(self.__empty_location_coordinates_text)
    
    def on_mouse_move(self, event):
        if self.__drag_manager.in_bounds(event.x, event.y):
            inc = self.__config["grid_size"] / self.__grid.dim
            self.coordinate_text.set("({},{})".format(int(event.x / inc), int(event.y / inc)))
        else:
            self.coordinate_text.set(self.__empty_location_coordinates_text)

    def drag_on_start(self, event):
        drag_manager, img_key = self.dragables[event.widget.find_closest(event.x, event.y)[0]]

        drag_manager.drag_image = self.all_images_tk_scaled[img_key]

        drag_manager.drag = self.canvas.create_image(event.x, event.y, image=drag_manager.drag_image)

        self.canvas.itemconfigure(drag_manager.drag, state="hidden")
        self.canvas.tag_lower(drag_manager.drag)
        self.selected = None

        #keep the currently selected draggable on the top
        for a in self.canvas_agents.values():
            try:
                self.canvas.tag_lower(a)
            except Exception:
                # If the draggable is not a valid argument for tag_lower, we ignore the error.
                pass
        for d in self.canvas_dirts.values():
            try:
                self.canvas.tag_lower(d)
            except Exception:
                # If the draggable is not a valid argument for tag_lower, we ignore the error.
                pass

    def drag_on_drop(self, event, drag_manager):
        #TODO: stream line to work with select

        inc = self.__config["grid_size"] / self.__grid.dim
        x = int(event.x / inc)
        y = int(event.y / inc)
        coord = Coord(x,y)
        #update the environment state
        colour, obj = drag_manager.get_key()
        print(colour, obj)
        if obj == "dirt":
            dirt1 =  self.__grid.dirt(colour)
            self.__grid.replace_dirt(coord, dirt1)
            if coord in self.canvas_dirts:
                self.canvas.delete(self.canvas_dirts[coord])
            self.canvas_dirts[coord] = drag_manager.drag
            self.canvas.tag_lower(self.canvas_dirts[coord])
        else:
            agent1 =  self.__grid.agent(colour, obj)
            self.__grid.replace_agent(coord, agent1)
            if coord in self.canvas_agents:
                self.canvas.delete(self.canvas_agents[coord])
            self.canvas_agents[coord] = drag_manager.drag
        print("INFO: drop", self.__grid.state[coord])
        
        self.select(event)
        self._redraw()

    def show_hide_side(self, state):
        for item in self.dragables.keys():
            self.canvas.itemconfigure(item, state=state)
        if state == "hidden":
            self.grid_scale_slider.pack_forget()
            self.mid_frame.pack_forget()
            self.info_frame.pack_forget()
        elif state == "normal":
            self.grid_scale_slider.pack(side="bottom")
            self.mid_frame.pack(side="left")
            self.info_frame.pack(side="left", expand=True)

    def user_mind(self):
        return self.buttons["difficulty"].get_difficulty()

    #resets the grid and enviroment
    def _reset(self):
        print("INFO: reset")
        self._reset_canvas(lines=False)
        self.__grid.reset(self.__grid.dim)
        self.reset_time_step()
        self.env = None

    def play(self) -> None:
        self._play()

    def _play(self):
        print("INFO: play")
        self.pack_buttons("stop", "pause", "fast")
        self.show_hide_side("hidden")
        self.deselect()
        self.running = True

        self.env = init_environment(self.__grid, self.agent_minds, self.current_user_mind)
        self.__grid.cycle = 0

        if self.after_hook: #prevent button spam
            self.__root.after_cancel(self.after_hook)
        time = int(self.__config["time_step"]*1000)
        self.after_hook = self.__root.after(time, self.simulate)

    def simulate(self):
        try: 
            if self.running:
                print("------------ cycle {} ------------ ".format(self.__grid.cycle))        
                self.env.evolveEnvironment()
                self.__grid.cycle += 1
                self.__root.after(0, self._redraw)

                time = int(self.__config["time_step"]*1000)
                self.after_hook = self.__root.after(time, self.simulate)
            
        except Exception:
            print("INFO: SIMULATION ERROR")
            self.__error()
            self.running = False
            self.__finish()

    def _stop(self):
        print("INFO: stop")
        self.reset = True
        self.reset_time_step()
        self.running = False
        self.pack_buttons("play", "reset", "fast", "difficulty", "guide", "save", "load")
        self.show_hide_side("normal")

    def _resume(self):
        print("INFO: resume")
        self.pack_buttons("stop", "pause", "fast")
        
        self.running = True
        
        if self.after_hook: #prevent button spam
            self.__root.after_cancel(self.after_hook)
        time = int(self.__config["time_step"]*1000)
        self.after_hook = self.__root.after(time, self.simulate)

    def _pause(self):
        print("INFO: pause")
        self.reset_time_step()
        self.pack_buttons("stop", "resume", "fast", "guide")
        self.running = False

    def _fast(self):
        self.__config["time_step_modifier"] /= 2.
        self.__config["time_step"] = self.__config["time_step_base"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

        print_simulation_speed_message(time_step=self.__config["time_step"])

    def reset_time_step(self):
        self.__config["time_step_modifier"] = 1.
        self.__config["time_step"] = self.__config["time_step_base"] * self.__config["time_step_modifier"] + self.__config["time_step_min"]

        print_simulation_speed_message(time_step=self.__config["time_step"])

    def _difficulty(self):
        self.current_user_mind = self.user_mind()