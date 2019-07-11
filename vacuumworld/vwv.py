


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:12:24 2019

@author: ben, Nausheen

from IPython import get_ipython
get_ipython().magic('reset -sf')
"""
from GridEnvironment import GridPhysics, GridAmbient,GridEnvironment
from GridSensor import CommunicationSensor,VisionSensor
from  Object import Dirt


from GridWorldAction import  DropDirtAction,ChangeOrientationAction,ForwardMoveMentAction,SpeakAction,MoveLeftAction,BroadcastAction,MoveRightAction,CleanDirtAction
from GridEnvironmentActuator import MovementActuator,CleaningDirtActuator, DropDirtActuator,CommunicationActuator
from GridPerception import Observation,GridVisionPerception,Message,ActionResultPerception
from VAgent import CleaningAgentMind,CleaningAgentBody 
from User import UserMind, UserBody 


from vwc import location, dirt, agent, coord
import tkinter as tk
import traceback
import os

from collections import OrderedDict as odict
from PIL import Image, ImageTk

#from Slider import Slider
#from vw import Environment
from Slider import Slider
from vw import PhysicalAllocationMap

#might need to change this for the real package...
PATH = os.path.dirname(__file__) + "/../"

WIDTH = 640
HEIGHT = 480
ROOT_FONT = "Verdana 10 bold" #font.Font(family='Helvetica', size=36, weight='bold')
BUTTON_PATH = PATH + "res/button.png"
LOCATION_AGENT_IMAGES_PATH = PATH + "res/locations/agent"
LOCATION_DIRT_IMAGES_PATH = PATH + "res/locations/dirt"
DEFAULT_LOCATION_SIZE = 60
DEFAULT_GRID_SIZE = 480


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

        button_image = ImageTk.PhotoImage(Image.open(BUTTON_PATH))
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

def _exit():
    root.destroy()
    
class CanvasDragManager:
    
    def __init__(self, name, env, canvas, item, on_start, on_drop):
        self.x = 0
        self.y = 0
        self.canvas = canvas
        
        self._on_start = on_start
        self._on_drop = on_drop
        self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drop)
        #self.canvas.configure(cursor="hand1")  
        self.drag_image = None
        self.drag = None
        self.dragging = False
        self.env = env
        self.name = name
        
    def _in_bounds(self, x,y):
        return x < DEFAULT_GRID_SIZE and x > 0 and y < DEFAULT_GRID_SIZE and y > 0
        
    def on_start(self, event):
        if not self.dragging:
            self._on_start(event)
            self.dragging = True
            self.x = event.x
            self.y = event.y
        
    def on_drag(self, event):
        
        inc = DEFAULT_GRID_SIZE / self.env.dim
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
        print('drop')
        if self._in_bounds(event.x, event.y):
            self._on_drop(event, self)
        self.dragging = False
        
    
class VWInterface(tk.Frame):
    
    def __init__(self, parent, env):
        super(VWInterface, self).__init__(parent)
        self.configure(background='white')
        self.canvas = tk.Canvas(self, width=DEFAULT_GRID_SIZE+DEFAULT_LOCATION_SIZE*4, 
                                height=DEFAULT_GRID_SIZE, 
                                bd=0, 
                                highlightthickness=0)
        #self.canvas.create_rectangle(0,0,481,481,fill="blue") # placeholder for grid
        #self.drag = self.canvas.create_rectangle(230,230,10,10, fill='yellow')

        self.buttons = {}
        button_image = tk.PhotoImage(file=BUTTON_PATH)
        self.button_frame = tk.Frame(self)
        self.buttons['back'] = VWButton(self.button_frame, button_image, _back, 'back')
        self.buttons['play'] = VWButton(self.button_frame, button_image, _play, 'play')
        self.buttons['back'].pack('left')
        self.buttons['play'].pack('left')

        self.canvas.configure(background='white')
        
        self.button_frame.pack()
        self.env = env
        
        self.placed_images = {}
        self.canvas_dirts = {}
        self.canvas_agents = {}
        
        self._init_dragables()
        self._init_options()
        
        self.grid_lines = []
        self._draw_grid(DEFAULT_GRID_SIZE, env.dim)
        self.canvas.pack()
        
    
    def _init_options(self):
        background = 'white'
        x = DEFAULT_GRID_SIZE + 2
        y = 5 * DEFAULT_LOCATION_SIZE
        w = DEFAULT_GRID_SIZE - 4 * DEFAULT_LOCATION_SIZE
        h = DEFAULT_GRID_SIZE - 5 * DEFAULT_LOCATION_SIZE
        self.options_frame = tk.Frame(self)
        print(x,y,w,h)
        self.canvas.create_window((x + w/2,y + h/2), width=w, height=h, window=self.options_frame)
        self.options_frame.configure(bg=background)
       
        self._size_slider_option(self.options_frame, background)        
        self._save_option(self.options_frame, background)
        self._load_option(self.options_frame, background)
    
    def _save_option(self, parent, bg):
        f = tk.Frame(parent, bg=bg)
        t = tk.Label(f, text=" save ", bg=bg, font = ROOT_FONT)
        t.pack(side='left')
        f.pack()
    
    def _load_option(self, parent, bg):
        f = tk.Frame(parent, bg=bg)
        t = tk.Label(f, text=" load ", bg=bg, font = ROOT_FONT)
        t.pack(side='left')
        f.pack()
    
    def _size_slider_option(self, parent, bg):
        f = tk.Frame(parent, bg=bg)
        t = tk.Label(f, text=" size ", bg=bg, font = ROOT_FONT)
        t.pack(side='left')
        increments = PhysicalAllocationMap.GRID_MAX_SIZE - PhysicalAllocationMap.GRID_MIN_SIZE
        self.grid_scale_slider = Slider(f, self.on_resize, None, increments * 16, 16, 
                                        increments=increments,
                                        start=(DEFAULT_GRID_SIZE/DEFAULT_LOCATION_SIZE) - PhysicalAllocationMap.GRID_MIN_SIZE)
        self.grid_scale_slider.pack(side='left')
        f.pack()
    
    def _reset_canvas(self):
        for line in self.grid_lines:
            self.canvas.delete(line)
        self.grid_lines.clear()
        for a in self.canvas_agents.values():
            self.canvas.delete(a)
        self.canvas_agents.clear()
        for d in self.canvas_dirts.values():
            self.canvas.delete(d)
        self.canvas_dirts.clear()
        self.placed_images.clear()
        
    def _draw_grid(self, size, env_dim):
        x = 0
        y = 0
        inc = size / env_dim
        for i in range(env_dim + 1):
           self.grid_lines.append(self.canvas.create_line(x,0,x,DEFAULT_GRID_SIZE))
           self.grid_lines.append(self.canvas.create_line(0,y,DEFAULT_GRID_SIZE,y))
           y += inc
           x += inc
           
        
    def _init_dragables(self):
        #load all images
        files = get_location_img_files(LOCATION_AGENT_IMAGES_PATH)
        names = [file.split('.')[0] for file in files]
        self.dragables = {}
        x = DEFAULT_GRID_SIZE + 2
        y = 0
        #for agents
        for name in names:
            file = os.path.join(LOCATION_AGENT_IMAGES_PATH, name) +  '.png'
            img = self._scale(Image.open(file), DEFAULT_LOCATION_SIZE)
            images = self._construct_images(img, name + '_')
            y = 0
            for img_name, img in images.items():
                tk_img = ImageTk.PhotoImage(img)
                item = self.canvas.create_image(x + img.width/2,y + img.height/2, image=tk_img)
                drag_manager = CanvasDragManager(img_name, self.env, self.canvas, item, self.drag_on_start, self.drag_on_drop)
                self.dragables[item] = (drag_manager, img, tk_img)
                y += DEFAULT_LOCATION_SIZE
            x += DEFAULT_LOCATION_SIZE
            
        #and for dirt...
        files = get_location_img_files(LOCATION_DIRT_IMAGES_PATH)
        names = [file.split('.')[0] for file in files]
        x = DEFAULT_GRID_SIZE + 2
        for name in names:
            file = os.path.join(LOCATION_DIRT_IMAGES_PATH, name) +  '.png'
            img = self._scale(Image.open(file), DEFAULT_LOCATION_SIZE)
            tk_img = ImageTk.PhotoImage(img)
            item = self.canvas.create_image(x + img.width/2,y + img.height/2, image=tk_img)
            drag_manager = CanvasDragManager(name, self.env, self.canvas, item, self.drag_on_start, self.drag_on_drop)
            self.dragables[item] = (drag_manager, img, tk_img)
            x += DEFAULT_LOCATION_SIZE
    
    def _construct_images(self, img, name):
        return odict({name + 'north':img, name + 'west':img.copy().rotate(90), name + 'south':img.copy().rotate(180), name + 'east':img.copy().rotate(270)})
    
    def _scale(self, img, lsize):
        scale = lsize / max(img.width, img.height)
        return img.resize((int(img.width  * scale), int(img.height * scale)), Image.BICUBIC)
    
    def on_resize(self, value):
        value =  value + PhysicalAllocationMap.GRID_MIN_SIZE
        if value != self.env.dim:
            print('resize', value)
            self.env.reset(value)
            self._reset_canvas()
            self._draw_grid(DEFAULT_GRID_SIZE, env.dim)
    
    def drag_on_start(self, event):
        drag_manager, image, _ = self.dragables[event.widget.find_closest(event.x, event.y)[0]]
        size = min(DEFAULT_LOCATION_SIZE, DEFAULT_GRID_SIZE  / self.env.dim)
        print('size', size)
        drag_manager.drag_image = ImageTk.PhotoImage(self._scale(image, size))
        drag_manager.drag = self.canvas.create_image(event.x, event.y, image=drag_manager.drag_image)
        self.canvas.itemconfigure(drag_manager.drag, state='hidden')
        self.canvas.tag_lower(drag_manager.drag)
        print(drag_manager.drag)
        #keep the currently selected draggable on the top
        for d in self.canvas_dirts.values():
            self.canvas.tag_lower(d)
        for a in self.canvas_agents.values():
            self.canvas.tag_lower(a)

    def drag_on_drop(self, event, drag_manager):

        inc = int(DEFAULT_GRID_SIZE / self.env.dim)
        x = int(event.x / inc) 
        y = int(event.y / inc)
        print(drag_manager.name, x,y)
        self.placed_images[(x,y)] = drag_manager.drag_image        
        #update the environment state
        colour, obj = drag_manager.name.split('_')
        if obj == 'dirt':
            dirt1 =  env.dirt(colour)
            env.replace_dirt((x,y), dirt1)
            if (x,y) in self.canvas_dirts:
                self.canvas.delete(self.canvas_dirts[(x,y)])
            self.canvas_dirts[(x,y)] = drag_manager.drag
            print(dirt1)
        else: #its and agent
            agent1 =  env.agent(colour, obj)
            env.replace_agent((x,y), agent1)
            if (x,y) in self.canvas_agents:
                self.canvas.delete(self.canvas_agents[(x,y)])
            self.canvas_agents[(x,y)] = drag_manager.drag
            print(agent1)
       
        '''
        for c,l in self.env.state.items():
            print(c,l)
        '''

def _play():
    print('play')
    actionList=[DropDirtAction,ForwardMoveMentAction,MoveRightAction,MoveLeftAction,CleanDirtAction,SpeakAction,BroadcastAction]
    phy = GridPhysics({VisionSensor:[Observation,GridVisionPerception,ActionResultPerception], 
                   CommunicationSensor:[Message]})
    
    agents=[]
    sensors=[]
    dirts=[]
    for i in range(env.dim):
      for j in range(env.dim):
         entity=env.state[coord(j,i)]       
         if(entity.agent):       
           act1=MovementActuator()
           s1=VisionSensor()
           sensors.append(s1)
           actuators=[]
           actuators.append(act1)
           
           if(entity.agent.colour!='user'):
               act2=CommunicationActuator()
               act3=CleaningDirtActuator()
               actuators.append(act2)
               actuators.append(act3)
               s2=CommunicationSensor()
               sensors.append(s2)
           
               ag=CleaningAgentBody(entity.agent.name,CleaningAgentMind(),actuators,[s1,s2],entity.agent.direction,entity.coordinate,entity.agent.colour)
                              
           else:                        
              act2=DropDirtActuator()
              actuators.append(act2)
              ag=UserBody(entity.agent.name,UserMind(),actuators,[s1],entity.agent.direction,entity.coordinate,entity.agent.colour)
               
             
             
           agents.append(ag)
         elif(entity.dirt):       
            d1= Dirt(entity.dirt.colour)
            dirts.append(d1)
             
    amb= GridAmbient(agents,dirts,env)
    e= GridEnvironment(phy,amb,actionList,sensors)
    e.simulate(10)

def _back():
    print('back')
    main_interface.pack_forget()
    main_menu.pack()
    
def run():  
    #required to avoid problems with running after errors (root must be destoryed!)
    
    
  #  import saveload
    
    try:
        INITIAL_ENVIRONMENT_DIM = 8

        global root
        root = tk.Tk()
        
        root.configure(background='white')
        
        global main_menu
        global main_interface
        global env
        env = PhysicalAllocationMap(INITIAL_ENVIRONMENT_DIM)
        
        #saveload.load('/test.vw', env)
        
        main_menu = VWMainMenu(root, _start, _exit)
        main_interface = VWInterface(root, env)
        
        root.mainloop()   
          
    except:
        root.destroy()
        traceback.print_exc()



        
run()
