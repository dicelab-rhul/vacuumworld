


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:12:24 2019

@author Benedict Wilkins
"""

import tkinter as tk
import traceback
import os
import time
from threading import Thread, Event

from collections import OrderedDict as odict
from PIL import Image, ImageTk


#from Slider import Slider
#from vw import Environment
from .slider import Slider
from .vw import Grid
from .vwenvironment import init as init_environment
from . import vwc
from . import saveload

#might need to change this for the real package...
PATH = os.path.dirname(__file__)
TIME_STEP_MIN = 1. / 2.**4
DEFAULT_TIME_STEP = 1 #in seconds
TIME_STEP = DEFAULT_TIME_STEP 
WIDTH = 640
HEIGHT = 480
ROOT_FONT = "Verdana 10 bold" #font.Font(family='Helvetica', size=36, weight='bold')
BUTTON_PATH = PATH + "/res/"
LOCATION_AGENT_IMAGES_PATH = PATH + "/res/locations/agent"
LOCATION_DIRT_IMAGES_PATH = PATH + "/res/locations/dirt"
DEFAULT_LOCATION_SIZE = 60
DEFAULT_GRID_SIZE = 480
BACKGROUND_COLOUR_SIDE = 'grey'
BACKGROUND_COLOUR_GRID = 'white'

DIFFICULTY_LEVELS = 3
INITIAL_ENVIRONMENT_DIM = 8
        
def get_location_img_files(path):
    return [file for file in os.listdir(path) if file.endswith(".png")]

class VWButton:
    
    def __init__(self, root, img, fun, text = None):
        self.img = img
        self.fun = fun
        self._button = tk.Button(root,
                                 text = text,
                                 bd=0,
                                 font = ROOT_FONT,
                                 fg='white',
                                 highlightthickness = 0,
                                 bg='white', 
                                 activebackground='white', 
                                 activeforeground='white',
                                 highlightcolor='white',
                                 compound = 'center',
                                 command = fun)
        self._button.config(image=img)
        
    def pack(self, side):
        self._button.pack(side=side)
        
class VWDifficultyButton(VWButton):
    
    def __init__(self, root, img, fun):
        self.imgs = [ImageTk.PhotoImage(img)]
        self.imgs.extend([self.next_image(img, i * (255/(DIFFICULTY_LEVELS-1))) for i in range(1, DIFFICULTY_LEVELS)])
        super(VWDifficultyButton, self).__init__(root, self.imgs[0], self.onclick)
        self.difficulty = 0
        self._rfun = fun
        
    def next_image(self, img, red):
        img_dif = Image.new("RGB", img.size)
        img_dif.paste(img)
        rr, gg, bb = img_dif.split()
        rr = rr.point(lambda p: p + red)
        img_dif = Image.merge("RGB", (rr, gg, bb)) 
        return ImageTk.PhotoImage(img_dif)

    def onclick(self):
        self.difficulty = (self.difficulty + 1) % len(self.imgs)
        self.img = self.imgs[self.difficulty]
        self._button.config(image=self.img)
        self._rfun() #update the global variable .... TODO change this
        
        
class VWMainMenu(tk.Frame):
    
    def __init__(self, root, _start, _exit):
        super(VWMainMenu,self).__init__(root)
        self.configure(background='white')
        self.canvas = tk.Canvas(self, width=480, 
                                height=480, 
                                bd=0, 
                                highlightthickness=0)
        self.canvas.create_rectangle(0,0,481,481,fill="blue") # placeholder for image
        self.canvas.pack()
        
        self.buttons = {}

        button_image = ImageTk.PhotoImage(Image.open(BUTTON_PATH + 'button.png'))
        self.button_frame = tk.Frame(self)
        
        self.buttons['start'] = VWButton(self.button_frame, button_image, _start, 'start')
        self.buttons['exit'] = VWButton(self.button_frame, button_image, _exit, 'exit')
        self.buttons['start'].pack('left')
        self.buttons['exit'].pack('left')
        self.button_frame.pack()

        self.pack()

def _start():
    main_menu.pack_forget()
    main_interface.pack()

def _in_bounds(x,y):
    return x < DEFAULT_GRID_SIZE and x > 0 and y < DEFAULT_GRID_SIZE and y > 0
    
    
class CanvasDragManager:
    
    def __init__(self, key, grid, canvas, item, on_start, on_drop):
        self.x = 0
        self.y = 0
        self.canvas = canvas
        
        self._on_start = on_start
        self._on_drop = on_drop
        self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drop)
        #self.canvas.configure(cursor="hand1")  
        
        self.key = key
        self.drag_image = None
        self.drag = None
        self.dragging = False
        self.grid = grid

    def on_start(self, event):
        if not self.dragging:
            self._on_start(event)
            self.dragging = True
            self.x = event.x
            self.y = event.y
        
    def on_drag(self, event):
        
        inc = DEFAULT_GRID_SIZE / self.grid.dim
        x = int(event.x / inc) * inc + (inc / 2) + 1
        y = int(event.y / inc) * inc + (inc / 2) + 1
        
        if x != self.x or y != self.y:
            if x <= DEFAULT_GRID_SIZE:
                self.canvas.itemconfigure(self.drag, state='normal')
            else:
                self.canvas.itemconfigure(self.drag, state='hidden')
            dx = x - self.x
            dy = y - self.y
            self.canvas.move(self.drag, dx, dy)
            self.x = x
            self.y = y

            
    def on_drop(self, event):
        #print('drop')
        if _in_bounds(event.x, event.y):
            self._on_drop(event, self)
        self.dragging = False
        
    
class VWInterface(tk.Frame):
    
    SIDE_PANEL_WIDTH = 4 * DEFAULT_LOCATION_SIZE
    
    def __init__(self, parent, grid):
        super(VWInterface, self).__init__(parent)
        self.configure(background=BACKGROUND_COLOUR_SIDE)
        self.canvas = tk.Canvas(self, width=DEFAULT_GRID_SIZE+DEFAULT_LOCATION_SIZE*4, 
                                height=DEFAULT_GRID_SIZE, 
                                bd=0, 
                                highlightthickness=0)
        #self.canvas.create_rectangle(0,0,481,481,fill="blue") # placeholder for grid
        #self.drag = self.canvas.create_rectangle(230,230,10,10, fill='yellow')

        buttons = self._init_buttons()


        self.canvas.configure(background=BACKGROUND_COLOUR_GRID)
        
        self.grid = grid
        
        self.canvas_dirts = {}
        self.canvas_agents = {}
        
        self.all_images = {} #stores all PIL images
        self.all_images_tk = {} #stores all tk images
        self.all_images_tk_scaled = {} #stores all tk images scale to fit grid
        self.grid_lines = [] #stores line objects
        
        self._init_images()
        self._init_dragables()
        self._init_options(buttons)

        self._draw_grid(grid.dim)
    
        self.canvas.pack()
        
        #bind keys for rotation
        parent.bind('<Left>', self.rotate_agent_left)
        parent.bind('<Right>', self.rotate_agent_right)
        parent.bind('<a>', self.rotate_agent_left)
        parent.bind('<d>', self.rotate_agent_right)
        
        self.canvas.bind('<Double-Button-1>', self.remove_top)
        self.canvas.bind('<Button-1>', self.select)
        
        self.currently_selected = None
        self.running = False
        self.rectangle_selected = None
    
    
    def deselect(self):
        self.selected = None
        if self.rectangle_selected:
            self.canvas.delete(self.rectangle_selected)
        self.rectangle_selected = None
    
    def select(self, event):
        if not self.running and _in_bounds(event.x, event.y):
            self.deselect()
            inc = DEFAULT_GRID_SIZE / self.grid.dim
            coordinate = vwc.coord(int(event.x / inc), int(event.y / inc))
            print("SELECT:", self.grid.state[coordinate])
            self.selected = grid.state[coordinate]
            xx = coordinate.x * inc
            yy = coordinate.y * inc
            self.rectangle_selected = self.canvas.create_rectangle((xx, yy, xx + inc, yy + inc), fill='', width=3)
     
    
    def remove_top(self, event):
        if not self.running and _in_bounds(event.x, event.y):
            print("remove top")           
            inc = DEFAULT_GRID_SIZE / self.grid.dim
            coordinate = vwc.coord(int(event.x / inc), int(event.y / inc))
            location = grid.state[coordinate]
            if location.agent:
                self.remove_agent(coordinate)
                self.grid.remove_agent(coordinate)
            elif grid.state[coordinate].dirt:
                self.remove_dirt(coordinate)
                self.grid.remove_dirt(coordinate)
                
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
    
    def rotate_agent(self, event, direction):
        #print('left', event)
        print(self.selected)
        if self.selected and self.selected.agent:
            self.remove_agent(self.selected.coordinate)
            new_orientation =  direction(self.selected.agent.orientation)
            inc = DEFAULT_GRID_SIZE / self.grid.dim
            tk_img = self.all_images_tk_scaled[(self.selected.agent.colour, new_orientation)]
            item = self.canvas.create_image(self.selected.coordinate.x * inc + inc/2, 
                                            self.selected.coordinate.y * inc + inc/2, image=tk_img)
            self.canvas_agents[self.selected.coordinate] = item
            self.grid.turn_agent(self.selected.coordinate, new_orientation)
            self.selected = self.grid.state[self.selected.coordinate]
            self._lines_to_front()
            
    def rotate_agent_left(self, event):
        self.rotate_agent(event, vwc.left)
            
    def rotate_agent_right(self, event):
        self.rotate_agent(event, vwc.right)
    
    def pack_buttons(self, *buttons, forget=True):
        if forget:
            for button in self.buttons.values():
               button._button.pack_forget()
        for button in buttons:
            self.buttons[button].pack('left')
    
    def _init_buttons(self):
        self.buttons = {}
       
        
        buttons = get_location_img_files(BUTTON_PATH)
        buttons = {b.split('.')[0]:b for b in buttons}
        
        
        self.button_frame = tk.Frame(self)
        self.button_frame.configure(bg='white')
        
        play_tk = tk.PhotoImage(file=BUTTON_PATH + buttons['play'])
        self.buttons['play'] = VWButton(self.button_frame, play_tk , _play)
        self.buttons['resume'] = VWButton(self.button_frame, play_tk, _resume)
        self.buttons['pause'] = VWButton(self.button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['pause']), _pause)
        self.buttons['stop'] = VWButton(self.button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['stop']), _stop)
        self.buttons['fast'] = VWButton(self.button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['fast']), _fast)
        self.buttons['reset'] = VWButton(self.button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['reset']), _reset)
        
        _img_dif = Image.open(BUTTON_PATH + buttons['difficulty'])
        self.buttons['difficulty'] = VWDifficultyButton(self.button_frame, _img_dif, _difficulty)
        #self.buttons['difficulty'] = VWButton(self.button_frame, _img_dif, _difficulty)
        
        self.buttons_tag = self.canvas.create_window((DEFAULT_GRID_SIZE + 2 + VWInterface.SIDE_PANEL_WIDTH/2,
                                                      DEFAULT_LOCATION_SIZE/2), 
                                                      width=VWInterface.SIDE_PANEL_WIDTH, 
                                                      height=DEFAULT_LOCATION_SIZE, 
                                                      window=self.button_frame)
                
        self.pack_buttons('play', 'reset', 'fast', 'difficulty')
        return buttons
    
    def _init_options(self, buttons):
        background = 'red'
        x = DEFAULT_GRID_SIZE + 2
        y = 6 * DEFAULT_LOCATION_SIZE
        w = VWInterface.SIDE_PANEL_WIDTH#DEFAULT_GRID_SIZE - 4 * DEFAULT_LOCATION_SIZE
        h = DEFAULT_GRID_SIZE - 6 * DEFAULT_LOCATION_SIZE
        self.options_frame = tk.Frame(self)
        self.options = self.canvas.create_window((x + w/2,y + h/2), width=w, height=h, window=self.options_frame)
        self.options_frame.configure(bg=background)
        
        self.options_button_frame = tk.Frame(self.options_frame, bg='white')
        self.buttons_options = {}
        self.buttons_options['save'] = VWButton(self.options_button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['save']), _save)
        self.buttons_options['load'] = VWButton(self.options_button_frame, tk.PhotoImage(file=BUTTON_PATH + buttons['load']), _load)
        self.buttons_options['save'].pack('left')
        self.buttons_options['load'].pack('right')
        files= saveload.files()
        self.load_option_variable = tk.StringVar()
        self.load_menu = tk.OptionMenu(self.options_button_frame, self.load_option_variable, '', *files, command=_load)
        self.load_menu.pack()
        self.options_button_frame.pack()
        
        self._size_slider_option(self.options_frame, background)
        #self._save_option(self.options_frame, background)
        #self._load_option(self.options_frame, background)
  
    
    def _size_slider_option(self, parent, bg):
        f = tk.Frame(parent, bg=bg)
        t = tk.Label(f, text=" size ", bg=bg, font = ROOT_FONT)
        t.pack(side='left')
        increments = Grid.GRID_MAX_SIZE - Grid.GRID_MIN_SIZE
        self.grid_scale_slider = Slider(f, self.on_resize, None, increments * 16, 16, 
                                        increments=increments,
                                        start=(DEFAULT_GRID_SIZE/DEFAULT_LOCATION_SIZE) - Grid.GRID_MIN_SIZE)
        self.grid_scale_slider.pack(side='left')
        f.pack()
    
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
        
    def _redraw(self):
        self._reset_canvas(lines=False, )
        inc = DEFAULT_GRID_SIZE / self.grid.dim
        for coord, location in grid.state.items():
            if location:
                if location.agent:
                    #print("AGENT:", coord, location)
                    tk_img = self.all_images_tk_scaled[(location.agent.colour, location.agent.orientation)]
                    item = self.canvas.create_image(coord.x * inc + inc/2, 
                                                    coord.y * inc + inc/2, image=tk_img)
                    self.canvas_agents[coord] = item
                    self.canvas.tag_lower(item) #keep the agent behind the grid lines
                    if coord in self.canvas_dirts: #keep the dirt behind the agent
                        self.canvas.tag_lower(self.canvas_dirts[coord]) 
                if location.dirt:
                    #print("DDDIRT:",  coord, location)
                    tk_img = self.all_images_tk_scaled[(location.dirt.colour, 'dirt')]
                    item = self.canvas.create_image(coord.x * inc + inc/2, coord.y * inc + inc/2, image=tk_img)
                    self.canvas_dirts[coord] = item
                    self.canvas.tag_lower(item) #keep dirt behind agents and grid lines
        #self._lines_to_front()
            
    def _draw_grid(self, env_dim, size = DEFAULT_GRID_SIZE):
        x = 0
        y = 0
        inc = size / env_dim
        for i in range(env_dim + 1):
           self.grid_lines.append(self.canvas.create_line(x,0,x,size))
           self.grid_lines.append(self.canvas.create_line(0,y,size,y))
           y += inc
           x += inc

    def _get_image_key(self, name):
        s = name.split("_")
        return (s[0], s[1])
    
    def _init_images(self):
        # agents
        files = get_location_img_files(LOCATION_AGENT_IMAGES_PATH)
        image_names = [file.split('.')[0] for file in files]
        
        for img_name in image_names:
            file = os.path.join(LOCATION_AGENT_IMAGES_PATH, img_name) +  '.png'
            img = self._scale(Image.open(file), DEFAULT_LOCATION_SIZE)
            images = self._construct_images(img, img_name + '_')
            for img_name, img in images.items():
                img_key = self._get_image_key(img_name)
                tk_img = ImageTk.PhotoImage(img)
                self.all_images[img_key] = img
                self.all_images_tk[img_key] = tk_img
                
        # dirts     
        files = get_location_img_files(LOCATION_DIRT_IMAGES_PATH)
        images_names = [file.split('.')[0] for file in files]

        for name in images_names:
            file = os.path.join(LOCATION_DIRT_IMAGES_PATH, name) +  '.png'
            img = self._scale(Image.open(file), DEFAULT_LOCATION_SIZE)
            img_key = self._get_image_key(name)
            tk_img = ImageTk.PhotoImage(img)
            self.all_images[img_key] = img
            self.all_images_tk[img_key] = tk_img
        
        self._scaled_tk()
            
    def _construct_images(self, img, name):
        #change this from magic strings... (use vwc orientation)
        return odict({name + 'north':img, 
                      name + 'west':img.copy().rotate(90), 
                      name + 'south':img.copy().rotate(180), 
                      name + 'east':img.copy().rotate(270)})
    
    def _scaled_tk(self):
        size = min(DEFAULT_LOCATION_SIZE, DEFAULT_GRID_SIZE  / self.grid.dim)
        for name, image in self.all_images.items():
            self.all_images_tk_scaled[name] = ImageTk.PhotoImage(self._scale(image, size))
        
    def _init_dragables(self):
        #load all images
        self.dragables = {}
        ix = DEFAULT_GRID_SIZE + DEFAULT_LOCATION_SIZE / 2 + 2
        iy = DEFAULT_LOCATION_SIZE +  DEFAULT_LOCATION_SIZE / 2
        keys = [('orange', 'north'), ('green', 'north'), ('white', 'north'), ('user', 'north'), ('orange', 'dirt'), ('green', 'dirt')]
        #print(self.all_images)
        for i, key in enumerate(keys):
            item = self.canvas.create_image(ix + (i % 2) * DEFAULT_LOCATION_SIZE, 
                                            iy + (int(i/2) % 3) * DEFAULT_LOCATION_SIZE, image=self.all_images_tk[key])
            drag_manager = CanvasDragManager(key, self.grid, self.canvas, item, self.drag_on_start, self.drag_on_drop)
            self.dragables[item] = (drag_manager, key)
            
    def _scale(self, img, lsize):
        scale = lsize / max(img.width, img.height)
        return img.resize((int(img.width  * scale), int(img.height * scale)), Image.BICUBIC)
    
    #resize the grid
    def on_resize(self, value):
        value =  value + Grid.GRID_MIN_SIZE
        if value != self.grid.dim:
            self.grid.reset(value)
            self._reset_canvas()
            self._scaled_tk() 
            self._draw_grid(grid.dim)

    def drag_on_start(self, event):
        drag_manager, img_key = self.dragables[event.widget.find_closest(event.x, event.y)[0]]

        drag_manager.drag_image = self.all_images_tk_scaled[img_key]#ImageTk.PhotoImage(self._scale(image, size))

        drag_manager.drag = self.canvas.create_image(event.x, event.y, image=drag_manager.drag_image)
        
        self.canvas.itemconfigure(drag_manager.drag, state='hidden')
        self.canvas.tag_lower(drag_manager.drag)
        self.selected = None 

        #keep the currently selected draggable on the top
        for a in self.canvas_agents.values():
            self.canvas.tag_lower(a)
        for d in self.canvas_dirts.values():
            self.canvas.tag_lower(d)


    def drag_on_drop(self, event, drag_manager):
        #TODO stream line to work with select
        
        inc = DEFAULT_GRID_SIZE / self.grid.dim
        x = int(event.x / inc) 
        y = int(event.y / inc)
        coord = vwc.coord(x,y)
        #update the environment state
        colour, obj = drag_manager.key
        if obj == 'dirt':
            dirt1 =  grid.dirt(colour)
            grid.replace_dirt(coord, dirt1)
            if coord in self.canvas_dirts:
                self.canvas.delete(self.canvas_dirts[coord])
            self.canvas_dirts[coord] = drag_manager.drag
        else: #its and agent
            agent1 =  grid.agent(colour, obj)
            grid.replace_agent(coord, agent1)
            if coord in self.canvas_agents:
                self.canvas.delete(self.canvas_agents[coord])
            self.canvas_agents[coord] = drag_manager.drag
        print("DROP:", self.grid.state[coord])

        self.select(event)
       
    def show_hide_side(self, state):
        for item in self.dragables.keys():
            self.canvas.itemconfigure(item, state=state)
        self.canvas.itemconfig(self.options, state=state)

    def user_mind(self):
        return self.buttons['difficulty'].difficulty

def _fast():
    global TIME_STEP
    TIME_STEP = max(TIME_STEP_MIN, TIME_STEP / 2.)
    print('fast', TIME_STEP)    
    
def _difficulty():
    global user_mind
    user_mind = main_interface.user_mind()

def _save(file=None):
    file = 'test1'
    print('save', file)
    saveload.save(grid, file)
    #TODO dont add the file more than once!
    main_interface.load_menu["menu"].add_command(label=file, command=tk._setit(main_interface.load_option_variable, file))

def _load(file):
    if len(file) > 0:
        print('load', file)
        grid.replace_all(saveload.load(file))
        main_interface._redraw()

#resets the grid and enviroment
def _reset():
    print('reset')
    global reset
    reset = True
    main_interface._reset_canvas(lines=False)
    grid.reset(grid.dim)
    reset_time_step()

def _play():
    print('play')
    play_event.set()
    main_interface.deselect()
    main_interface.running = True
    main_interface.pack_buttons('stop', 'pause', 'fast')
    main_interface.show_hide_side('hidden')
  
def _stop():
    print('stop')
    global reset
    reset = True
    play_event.clear()
    reset_time_step()
    main_interface.running = False
    main_interface.pack_buttons('play', 'reset', 'fast', 'difficulty')
    main_interface.show_hide_side('normal')

def _resume():
    print('resume')
    play_event.set()
    main_interface.pack_buttons('stop', 'pause','fast')
    
def _pause():
    print('pause')
    play_event.clear()
    reset_time_step()
    main_interface.pack_buttons('stop', 'resume','fast')
        
def _back():
    print('back')
    play_event.clear()
    main_interface.pack_forget()
    main_menu.pack()

def _error(*_):
    traceback.print_exc()
    _finish()
    
def _finish():
    root.destroy()
    global finish
    finish = True
    
def reset_time_step():
    global TIME_STEP, DEFAULT_TIME_STEP
    TIME_STEP = DEFAULT_TIME_STEP

def run(_minds):  
    #required to avoid problems with running after errors (root must be destoryed!)
    
    
  #  import saveload
    
    try:
        global root
        tk.Tk.report_callback_exception = _error
        
        root = tk.Tk()
        root.title("Vacuum World")
        root.protocol("WM_DELETE_WINDOW", _finish)
        root.configure(background='white')
        
        global main_menu
        global main_interface
        global grid
        global minds
        minds = _minds
        
        global user_mind
        user_mind = 0
        
        grid = Grid(INITIAL_ENVIRONMENT_DIM)

        #saveload.load('/test.vw', grid)
        
        main_menu = VWMainMenu(root, _start, _finish)
        main_interface = VWInterface(root, grid)
        #print(dir(main_menu.canvas))
        
        global env_thread
        global play_event, finish, reset

        reset = True
        finish = False

        play_event = Event()
        
        env_thread = Thread(target=simulate, daemon=True)
        env_thread.start()

        root.mainloop()   
    except:
        _error()

#TODO, be able to select user mind from gui 


def simulate():  
    try:
        def wait():
            play_event.wait()
            return play_event.is_set()
        global reset
        global should_update
        global user_mind
        
        while wait() and not finish:
            if reset:
                global env
                env = init_environment(grid, minds, user_mind)
                grid.cycle = 0
                reset = False
                
            time.sleep(TIME_STEP)
            print("evolve", grid.cycle)
            #for k,v in grid.state.items():
            #    print(k,v)
            env.evolveEnvironment()
            grid.cycle += 1
            if not finish:
                root.after(0, main_interface._redraw)

    except:
        _error()
