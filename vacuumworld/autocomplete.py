#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CREDIT: http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
"""

import tkinter as tk
import re

class AutocompleteEntry(tk.Entry):
    
    def __init__(self, lista, height, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.dropdown_parent = args[0]
        self.lista = lista
        self.var = self["textvariable"]
        self.font = kwargs.get('font', None)
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.height = int(height)
        #self.bind("<Key>", self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.lb = None
        self.lb_up = False

    def changed(self, *args):
        #print(args)
        #name, index, mode = args
        #print("changed", name, index, mode, self.var.get())

        if self.var.get() == '':
            if self.lb:
                self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = tk.Listbox(self.dropdown_parent, font=self.font, height=self.height)
                    
                    self.lb.bind("<Double-Button-1>", self.selection)
                    #print(self.winfo_x(), self.winfo_y()+self.winfo_height())
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    #self.lb.place(x=381, y=300)
                    self.lb_up = True
                
                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):
        #print(event)
        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def up(self, event):
        if self.lb_up and not self.lb.curselection() == ():
            #print('up', self.lb.curselection())
            index = self.lb.curselection()[0]
            if index >= 0:
                self.lb.yview_scroll(-1, "units")
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 


    def down(self, event):
        if self.lb_up:
            #print('down', self.lb.curselection(), len(self.lista))
            if self.lb.curselection() == ():
                self.lb.selection_set(first=0)
                self.lb.activate(0) 
                return

            index = self.lb.curselection()[0]
            if int(index) + 1 < len(self.lista):
                if int(index) + 1 >= self.height:
                    self.lb.yview_scroll(1, "units") 
                    #print('scroll')
                
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 
                
    def comparison(self):
        #print("compare")
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

if __name__ == '__main__':
    root = tk.Tk()
    lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 
             'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 
             'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 
             'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 
             'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 
             'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the',
             'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    tk.Button(text='nothing').grid(row=1, column=0)
    tk.Button(text='nothing').grid(row=2, column=0)
    tk.Button(text='nothing').grid(row=3, column=0)

    root.mainloop()