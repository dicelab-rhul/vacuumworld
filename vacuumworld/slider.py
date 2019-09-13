#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 20:05:16 2019

@author: ben
"""
import tkinter as tk

class Slider(tk.Canvas):
    
    def __init__(self, parent, release_callback, slide_callback, img, width, height, increments = 0, slider_width = 8, start = 0, **kwargs):
        super(Slider, self).__init__(parent, width=width, height=height, bd=0, highlightthickness=0, relief='ridge', bg='white', **kwargs)
        self.release_callback = release_callback
        self.slide_callback = slide_callback
        
        self.increments = increments
        self.slider_image = img
        self.slide_item_dim = slider_width
        
        self.x = start #real position of the slider
        self.inc = 0   #incremental position of the slider [0-increments] 
        if start > width:
            start = width - self.slide_item_dim/2
        if increments: 
            dx = int((width - self.slide_item_dim) / self.increments)
            self.x = start * dx
            self.inc = start
            

        self.background_item = self.create_rectangle(0,0, width-1, height-1, fill='white')
        self.slider_item = self.create_rectangle(self.x, 0, self.x + self.slide_item_dim, height, fill='black') #self.create_image(img, 0, 0)
        self.bind("<ButtonPress-1>", self.on_start)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
    
    def set_position(self, inc, callback=True):
        if inc != self.inc:
            inc = max(0, min(inc, self.increments))
            width = self.winfo_width() - self.slide_item_dim
            old_x = self.x
            self.x = inc * int(width / self.increments)
            self.inc = inc
            self.move(self.slider_item, self.x - old_x, 0)
            if callback:
                self.slide_callback(self.inc)
                self.release_callback(self.inc)
        
    def _move_slider(self, event):
        width = self.winfo_width() - self.slide_item_dim
        x = event.x     
        if x > 0 and x < width:
            if self.increments:
                inc = int(width / self.increments)
                self.inc = int(x / inc) 
                x = self.inc * inc

            dx = x - self.x
            if dx != 0:
                self.move(self.slider_item, dx, 0)
                self.slide_callback(self.inc)
                self.x = x
    
    def on_start(self, event):
        self._move_slider(event)
        
    def on_drag(self, event):
        self._move_slider(event)
        
    def on_drop(self, event):
        x = self.x
        if self.increments:
            x = self.inc
        self.release_callback(int(x))
       
