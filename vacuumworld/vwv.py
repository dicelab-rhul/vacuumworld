


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
from .autocomplete import AutocompleteEntry
from .vw import Grid
from .vwenvironment import init as init_environment
from . import vwc
from . import saveload
from . import vwuser

#might need to change this for the real package...
PATH = os.path.dirname(__file__)
TIME_STEP_MIN = 0.04
TIME_STEP_BASE = 1. - TIME_STEP_MIN #in seconds
TIME_STEP = TIME_STEP_BASE
TIME_STEP_MODIFIER = 1.


WIDTH = 480     #default - depends on layout manager
HEIGHT = 480    #default - depends on layout manager

BUTTON_PATH = PATH + "/res/"
LOCATION_AGENT_IMAGES_PATH = PATH + "/res/locations/agent"
LOCATION_DIRT_IMAGES_PATH = PATH + "/res/locations/dirt"
MAIN_MENU_IMAGE_PATH = PATH + "/res/start_menu.png"

DEFAULT_LOCATION_SIZE = 60
DEFAULT_GRID_SIZE = 480
DEFAULT_BUTTON_SIZE = 50

SCALE_MODIFIER = 1

GRID_SIZE = DEFAULT_GRID_SIZE * SCALE_MODIFIER
LOCATION_SIZE = DEFAULT_LOCATION_SIZE * SCALE_MODIFIER
BUTTON_SIZE = DEFAULT_BUTTON_SIZE * SCALE_MODIFIER
ROOT_FONT = ('Verdana', int(10 * SCALE_MODIFIER), '')

BACKGROUND_COLOUR_SIDE = 'white'
BACKGROUND_COLOUR_GRID = 'white'

DIFFICULTY_LEVELS = len(vwuser.USERS)
INITIAL_ENVIRONMENT_DIM = 8

def get_location_img_files(path):
    return [file for file in os.listdir(path) if file.endswith(".png")]

class VWButton:

    def __init__(self, root, img, fun, text = None):
        self.img = ImageTk.PhotoImage(img)
        self.fun = fun
        self._button = tk.Button(root, text = text, bd=0, font = ROOT_FONT, fg='white',
                                 highlightthickness = 0, bg='white', activebackground='white',
                                 activeforeground='white', highlightcolor='white', compound = 'center',
                                 command = fun)
        self._button.config(image=self.img)

    def pack(self, side):
        self._button.pack(side=side)
        
    def grid(self, row, col):
        self._button.grid(row=row,column=col)
        
    def destroy(self):
        self._button.destroy()
        self.img.destroy()

class VWDifficultyButton(VWButton):

    def __init__(self, root, img, fun):
        self.imgs = [ImageTk.PhotoImage(img)]
        self.imgs.extend([self.next_image(img, i * (255/(DIFFICULTY_LEVELS-1))) for i in range(1, DIFFICULTY_LEVELS)])
        super(VWDifficultyButton, self).__init__(root, img, self.onclick)
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
        self.canvas = tk.Canvas(self, width = GRID_SIZE + 1,
                                height = GRID_SIZE + 1,
                                bd=0,
                                highlightthickness=0)
        #self.canvas.create_rectangle(0,0,481,481,fill="blue") # placeholder for image


        self.img_tk = ImageTk.PhotoImage(Image.open(MAIN_MENU_IMAGE_PATH).resize((int(GRID_SIZE), int(GRID_SIZE)), Image.BICUBIC))
        self.image = self.canvas.create_image(GRID_SIZE/2,GRID_SIZE/2,image=self.img_tk)
        
        self.button_frame = tk.Frame(self)
        
        #self.canvas.create_window(WIDTH/2, HEIGHT-100, window =  self.button_frame)
        self.canvas.pack()
        self.buttons = {}

        button_image = Image.open(BUTTON_PATH + 'button.png')
        button_image = button_image.resize((int(button_image.width * SCALE_MODIFIER), int(button_image.height * SCALE_MODIFIER)), Image.BICUBIC)
        self.buttons['start'] = VWButton(self.button_frame, button_image, _start, 'start')
        self.buttons['exit'] = VWButton(self.button_frame, button_image, _exit, 'exit')
        
        self.buttons['start'].pack('left')
        self.buttons['exit'].pack('left')
        self.button_frame.pack()

        self.pack()


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

        inc = GRID_SIZE / self.grid.dim
        x = int(event.x / inc) * inc + (inc / 2) + 1
        y = int(event.y / inc) * inc + (inc / 2) + 1

        if x != self.x or y != self.y:
            if x <= GRID_SIZE:
                self.canvas.itemconfigure(self.drag, state='normal')
            else:
                self.canvas.itemconfigure(self.drag, state='hidden')
            dx = x - self.x
            dy = y - self.y
            self.canvas.move(self.drag, dx, dy)
            self.x = x
            self.y = y


    def on_drop(self, event):
        if _in_bounds(event.x, event.y):
            self._on_drop(event, self)
        self.dragging = False


class VWInterface(tk.Frame):

    def __init__(self, parent, grid):
        super(VWInterface, self).__init__(parent)
        self.parent = parent
        self.configure(background=BACKGROUND_COLOUR_SIDE)
        self.canvas = tk.Canvas(self, width=GRID_SIZE+LOCATION_SIZE+4,
                                height=GRID_SIZE + 1,
                                bd=0,
                                highlightthickness=0)
        #self.canvas.create_rectangle(0,0,481,481,fill="blue") # placeholder for grid
        #self.drag = self.canvas.create_rectangle(230,230,10,10, fill='yellow')

        self._init_buttons()

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

        self._draw_grid(grid.dim, GRID_SIZE)

        self.canvas.grid(row=0,column=0) #packing

        #bind keys for rotation
        parent.bind('<Left>', self.rotate_agent_left)
        parent.bind('<Right>', self.rotate_agent_right)
        parent.bind('<a>', self.rotate_agent_left)
        parent.bind('<d>', self.rotate_agent_right)
        self.parent = parent

        self.canvas.bind('<Double-Button-1>', self.remove_top)
        self.canvas.bind('<Button-1>', self.select)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_leave_canvas)
        
        
        self.currently_selected = None
        self.running = False
        self.rectangle_selected = None
        self.selected = None
        
    def _init_buttons(self):
        self.buttons = {}

        bg = 'white'
        buttons = get_location_img_files(BUTTON_PATH)
        buttons = {b.split('.')[0]:b for b in buttons}

        self.button_frame = tk.Frame(self, bg=bg)

        
        play_img = self._scale(Image.open(BUTTON_PATH + buttons['play']), BUTTON_SIZE)

        #left side contains buttons and slider
        self.left_frame = tk.Frame(self.button_frame, bg=bg)
        self.slider_frame = tk.Frame(self.left_frame, bg=bg)
        self.control_buttons_frame = tk.Frame(self.left_frame, bg=bg)
        
        self.buttons['play'] = VWButton(self.control_buttons_frame, play_img , _play)
        self.buttons['resume'] = VWButton(self.control_buttons_frame, play_img, _resume)
        self.buttons['pause'] = VWButton(self.control_buttons_frame, self._scale(Image.open(BUTTON_PATH + buttons['pause']), BUTTON_SIZE), _pause)
        self.buttons['stop'] = VWButton(self.control_buttons_frame, self._scale(Image.open(BUTTON_PATH + buttons['stop']), BUTTON_SIZE), _stop)
        self.buttons['fast'] = VWButton(self.control_buttons_frame, self._scale(Image.open(BUTTON_PATH + buttons['fast']), BUTTON_SIZE), _fast)
        self.buttons['reset'] = VWButton(self.control_buttons_frame, self._scale(Image.open(BUTTON_PATH + buttons['reset']), BUTTON_SIZE), _reset)

        
        dif_img = self._scale(Image.open(BUTTON_PATH + buttons['difficulty']), BUTTON_SIZE)
        self.buttons['difficulty'] = VWDifficultyButton(self.control_buttons_frame, dif_img, _difficulty)
        
        self.pack_buttons('play', 'reset', 'fast', 'difficulty', forget=False)
        
        #init the slider
        self._init_size_slider(self.slider_frame, bg)
        
        self.slider_frame.grid(row=0, column=0)#.pack(side='top')
        self.control_buttons_frame.grid(row=1, column=0, sticky=tk.W)#.pack(side='bottom')

        self.left_frame.pack(side='left', fill=tk.X)
  
        #middle contains save and load
        self.mid_frame = tk.Frame(self.button_frame, bg=bg)
        self.saveload_frame = tk.Frame(self.mid_frame, bg=bg)
    
        #buttons
        self.buttons['save'] = VWButton(self.saveload_frame, self._scale(Image.open(BUTTON_PATH + buttons['save']), BUTTON_SIZE), lambda: _save(self.load_menu))
        self.buttons['load'] = VWButton(self.saveload_frame, self._scale(Image.open(BUTTON_PATH + buttons['load']), BUTTON_SIZE), lambda: _load(self.load_menu))
        
        
        #entry box
        files = saveload.files()
        self.load_menu = AutocompleteEntry(files, 3, self.mid_frame, font=ROOT_FONT)
        self.load_menu.bind('<Button-1>', lambda _: self.deselect())
        self.load_menu.pack(side='top')
    
        self.pack_buttons('save', 'load', forget=False)
        self.saveload_frame.pack(side='bottom')
        self.mid_frame.pack(side='left')

        #init information frame
        self.info_frame = tk.Frame(self.button_frame, bg=bg)
        
        _size_frame = tk.Frame(self.info_frame, bg=bg)
        self.size_text = tk.StringVar()
        self.size_text.set(str(INITIAL_ENVIRONMENT_DIM))
        self.size_label = tk.Label(_size_frame, textvariable=self.size_text, width=2, font=ROOT_FONT, bg=bg)
        self.size_label.grid(row=0, column=1, sticky=tk.E)
        
        _size = tk.StringVar()
        _size.set("size:")
        _size_label =  tk.Label(_size_frame, textvariable=_size, font=ROOT_FONT, bg=bg)
        _size_label.grid(row=0, column=0, sticky=tk.W)
        _size_frame.grid(row=0, column=0, stick=tk.W)
        
        self.coordinate_text = tk.StringVar()
        self.coordinate_text.set("(-,-)")
        self.coordinate_label = tk.Label(self.info_frame, textvariable=self.coordinate_text, font=ROOT_FONT, bg=bg)
        self.coordinate_label.grid(row=1, column=0, sticky=tk.W)

        self.info_frame.pack(side='left', expand=True)
        self.button_frame.grid(row=1, column=0, pady=3, sticky=tk.W+tk.E)

        return buttons
    
    
    def _init_size_slider(self, parent, bg, length=200):
        #f = tk.Frame(parent, bg=bg)
        #t = tk.Label(f, text=" size ", bg=bg, font = ROOT_FONT)
        #t.pack(side='left')
        increments = Grid.GRID_MAX_SIZE - Grid.GRID_MIN_SIZE
        self.grid_scale_slider = Slider(parent, self.on_resize, self.on_resize_slide, None, length * SCALE_MODIFIER, 16 * SCALE_MODIFIER,
                                        slider_width = length * SCALE_MODIFIER / (increments * 3),
                                        increments=increments,
                                        start=(GRID_SIZE/LOCATION_SIZE) - Grid.GRID_MIN_SIZE)
        self.grid_scale_slider.pack(side='top')
        #f.pack(side='bottom')
        
    def _init_dragables(self):
        #load all images
        keys = [('white', 'north'), ('orange', 'north'), ('green', 'north'), ('user', 'north'), ('orange', 'dirt'), ('green', 'dirt')]
        self.dragables = {}

        ix = GRID_SIZE + LOCATION_SIZE / 2 + 2
        iy = LOCATION_SIZE / 2 + 4
        
        #print(self.all_images)
        for i, key in enumerate(keys):
            item = self.canvas.create_image(ix, iy + i * LOCATION_SIZE, image=self.all_images_tk[key])
            drag_manager = CanvasDragManager(key, self.grid, self.canvas, item, self.drag_on_start, self.drag_on_drop)
            self.dragables[item] = (drag_manager, key)

    def deselect(self):
        self.selected = None
        if self.rectangle_selected:
            self.canvas.delete(self.rectangle_selected)
        self.rectangle_selected = None

    def select(self, event):
        if not self.running and _in_bounds(event.x, event.y):
            self.deselect()
            self.focus()
            inc = GRID_SIZE / self.grid.dim
            coordinate = vwc.coord(int(event.x / inc), int(event.y / inc))
            print("SELECT:", self.grid.state[coordinate])
            self.selected = grid.state[coordinate]
            xx = coordinate.x * inc
            yy = coordinate.y * inc
            self.rectangle_selected = self.canvas.create_rectangle((xx, yy, xx + inc, yy + inc), fill='', width=3)


    def remove_top(self, event):
        if not self.running and _in_bounds(event.x, event.y):
            print("remove top")
            inc = GRID_SIZE / self.grid.dim
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
        if self.selected and self.selected.agent:
            print(self.selected)
            self.remove_agent(self.selected.coordinate)
            new_orientation =  direction(self.selected.agent.orientation)
            inc = GRID_SIZE / self.grid.dim
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
               button._button.grid_remove()
        for i in range(len(buttons)):
            self.buttons[buttons[i]]._button.grid(row=0, column=i, sticky=tk.W)

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
        self._reset_canvas(lines=False)
        inc = GRID_SIZE / self.grid.dim
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

    def _draw_grid(self, env_dim, size):
        x = 0
        y = 0
        inc = size / env_dim
        for i in range(env_dim + 1):
           self.grid_lines.append(self.canvas.create_line(x,0,x,size+1))
           self.grid_lines.append(self.canvas.create_line(0,y,size+1,y))
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
            img = self._scale(Image.open(file), LOCATION_SIZE)
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
            img = self._scale(Image.open(file), LOCATION_SIZE)
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
        size = min(LOCATION_SIZE, GRID_SIZE  / self.grid.dim)
        #print("SIZE: ", size)
        for name, image in self.all_images.items():
            self.all_images_tk_scaled[name] = ImageTk.PhotoImage(self._scale(image, size))

    def _scale(self, img, lsize):
        scale = lsize / max(img.width, img.height)
        return img.resize((int(img.width * scale), int(img.height * scale)), Image.BICUBIC)

    #resize the grid
    def on_resize(self, value):
        value =  value + Grid.GRID_MIN_SIZE
        if value != self.grid.dim:
            self.grid.reset(value)
            self._reset_canvas()
            self._scaled_tk()
            self._draw_grid(grid.dim, GRID_SIZE)
            
    def on_resize_slide(self, value):
        self.size_text.set(str(value + Grid.GRID_MIN_SIZE))
    
    def on_leave_canvas(self, event):
        self.coordinate_text.set('(-,-)')
    
    def on_mouse_move(self, event):
        if _in_bounds(event.x, event.y):
            inc = GRID_SIZE / self.grid.dim
            self.coordinate_text.set('({},{})'.format(int(event.x / inc), int(event.y / inc)))
        else:
            self.coordinate_text.set('(-,-)')

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

        inc = GRID_SIZE / self.grid.dim
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
            self.canvas.tag_lower(self.canvas_dirts[coord])
        else: #its and agent
            agent1 =  grid.agent(colour, obj)
            grid.replace_agent(coord, agent1)
            if coord in self.canvas_agents:
                self.canvas.delete(self.canvas_agents[coord])
            self.canvas_agents[coord] = drag_manager.drag
        print("INFO: drop", self.grid.state[coord])
        
        self.select(event)

    def show_hide_side(self, state):
        for item in self.dragables.keys():
            self.canvas.itemconfigure(item, state=state)
        if state == 'hidden':
            self.grid_scale_slider.pack_forget()
            self.mid_frame.pack_forget()
            self.info_frame.pack_forget()
        elif state == 'normal':
            self.grid_scale_slider.pack(side='bottom')
            self.mid_frame.pack(side='left')
            self.info_frame.pack(side='left', expand=True)
        #self.canvas.itemconfig(self.options, state=state)

    def user_mind(self):
        return self.buttons['difficulty'].difficulty
    

def _fast():
    global TIME_STEP, TIME_STEP_BASE, TIME_STEP_MODIFIER
    TIME_STEP_MODIFIER /= 2.
    TIME_STEP = TIME_STEP_BASE * TIME_STEP_MODIFIER + TIME_STEP_MIN
    print("INFO: simulation speed set to {:1.4f} s/cycle".format(TIME_STEP))

def reset_time_step():
    global TIME_STEP, TIME_STEP_BASE, TIME_STEP_MODIFIER
    TIME_STEP_MODIFIER = 1.
    TIME_STEP = TIME_STEP_BASE * TIME_STEP_MODIFIER + TIME_STEP_MIN
    print("INFO: simulation speed set to {:1.4f} s/cycle".format(TIME_STEP))

def _difficulty():
    global user_mind
    user_mind = main_interface.user_mind()

def _save(saveloadmenu):
    file = saveloadmenu.var.get()
    if len(file) > 0:
        print('INFO: save', file)
        saveload.save(grid, file)
        saveloadmenu.lista = saveload.files()

def _load(saveloadmenu):
    file = saveloadmenu.var.get()
    if len(file) > 0:
        if not file.endswith('.vw'):
            file = file + ".vw"
        if file in saveloadmenu.lista:
            print('INFO: load:', file)
            data = saveload.load(file)
            if data is not None:
                main_interface.grid_scale_slider.set_position(data.dim - grid.GRID_MIN_SIZE)
                grid.replace_all(data)
                main_interface._redraw()

            
            
    
#resets the grid and enviroment
def _reset():
    print('INFO: reset')
    global reset
    reset = True
    main_interface._reset_canvas(lines=False)
    grid.reset(grid.dim)
    reset_time_step()

def _play():
    print('INFO: play')

    play_event.set()
    main_interface.pack_buttons('stop', 'pause', 'fast')
    main_interface.show_hide_side('hidden')
    main_interface.deselect()
    main_interface.running = True
              

def _stop():
    print('INFO: stop')
    global reset
    reset = True
    play_event.clear()
    reset_time_step()
    main_interface.running = False
    main_interface.pack_buttons('play', 'reset', 'fast', 'difficulty', 'save', 'load')
    main_interface.show_hide_side('normal')

def _resume():
    print('INFO: resume')
    
    play_event.set()
    main_interface.pack_buttons('stop', 'pause','fast')

def _pause():
    print('INFO: pause')
    play_event.clear()
    reset_time_step()
    main_interface.pack_buttons('stop', 'resume','fast')

def _back():
    print('INFO: back')
    play_event.clear()
    main_interface.pack_forget()
    main_menu.pack()

def _error(*_):
    traceback.print_exc()

def _finish():
    global root
    root.destroy()
    global finish
    finish = True
    
def _start():
    main_menu.pack_forget()
    main_interface.pack()

def _in_bounds(x,y):
    return x < GRID_SIZE and x > 0 and y < GRID_SIZE and y > 0

def _scale(scale):
    global SCALE_MODIFIER, GRID_SIZE, LOCATION_SIZE, BUTTON_SIZE, ROOT_FONT
    SCALE_MODIFIER = scale
    GRID_SIZE = DEFAULT_GRID_SIZE * SCALE_MODIFIER
    LOCATION_SIZE = DEFAULT_LOCATION_SIZE * SCALE_MODIFIER
    BUTTON_SIZE = DEFAULT_BUTTON_SIZE * SCALE_MODIFIER
    ROOT_FONT = ('Verdana', int(10 * SCALE_MODIFIER), '')

def run(_minds, skip = False, play = False, speed = 0, load = None, scale = 1):
    assert(speed >= 0 and speed <= 1)
    assert scale > 0

   
  
    global root
    tk.Tk.report_callback_exception = _error
    root = tk.Tk()
    root.title("Vacuum World")
    root.protocol("WM_DELETE_WINDOW", _finish)
    root.configure(background='white')
    
    _scale(scale)
   
    try:
        global main_menu
        global main_interface
        global grid
        global minds
        minds = _minds

        global user_mind
        user_mind = 0

        grid = Grid(INITIAL_ENVIRONMENT_DIM)
        saveload.init()
        #saveload.load('/test.vw', grid)
        
        if not skip:    
            main_menu = VWMainMenu(root, _start, _finish)
            main_interface = VWInterface(root, grid)
        else:
            main_interface = VWInterface(root, grid)
            main_interface.pack()
            
        if play:
            if load is None:
                raise ValueError("argument \"load\" must be specified if argument play = True")
            load = saveload.format_file(load)
            files = saveload.files()
            if not load in files:
                raise ValueError("invalid file name: " + str(load) + " valid files include:" + str(files))
            print("INFO: autoplay enabled")
            
        if load is not None:
            grid.replace_all(saveload.load(load))
            main_interface._redraw()
            print("INFO: successfully loaded: ", load)
            
        global env_thread
        global play_event, finish, reset

        reset = True
        finish = False

        play_event = Event()

        env_thread = Thread(target=simulate, daemon=True)
        env_thread.start()
        
        #set up simulation speed
        global TIME_STEP
        global TIME_STEP_MODIFIER
        TIME_STEP_MODIFIER = 1 - speed
        TIME_STEP = TIME_STEP_BASE * TIME_STEP_MODIFIER + TIME_STEP_MIN
        print("INFO: simulation speed set to {:1.4f} s/cycle".format(TIME_STEP))
                
        if play:
            _play()
        root.mainloop()
        
    except:
        _error()
        _finish()




#TODO, be able to select user mind from gui

def simulate():
    try:
        def wait():
            should_sleep = not play_event.is_set()
            play_event.wait()
            if should_sleep:
                with Sleep(TIME_STEP*1000):
                     pass
            return True
        
        global reset
        global should_update
        global user_mind
        
        while wait() and not finish:
            #with TimeRecord(str(TIME_STEP)): #ms:
            with Sleep(TIME_STEP*1000):
                if reset:
                    global env
                    env = init_environment(grid, minds, user_mind)
                    grid.cycle = 0
                    reset = False
                
                print("------------ cycle {} ------------ ".format(grid.cycle))
                
                env.evolveEnvironment()
            
                grid.cycle += 1
                if not finish:
                    root.after(0, main_interface._redraw)
    except:
        print("INFO: SIMULATION ERROR")
        _error()
        root.after(0, _finish)
        
t = lambda: int(round(time.time() * 1000))

class Sleep:
    
    def __init__(self, wait):
        self.wait = wait
       
    def __enter__(self):
        self.start = t()
        self.finish = self.start + self.wait
    
    def __exit__(self, type, value, traceback):
        while t() < self.finish:
            time.sleep(1./1000.)  
            
class TimeRecord:
    
    def __init__(self, name):
        self._name = name
    
    def __enter__(self,):
        self._t = time.time() * 1000
    
    def __exit__(self, type, value, traceback):
        print("INFO: {0} time: {1}".format(self._name, time.time()  * 1000 - self._t))