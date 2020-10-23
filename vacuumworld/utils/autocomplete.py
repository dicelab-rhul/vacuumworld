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
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.lb = None
        self.lb_up = False

    def changed(self, *_):
        if self.var.get() == '':
            if self.lb:
                self.lb.destroy()
            self.lb_up = False
        else:
            self.check_words()
                    
    def check_words(self):
        words = self.comparison()
        if words:            
            if not self.lb_up:
                self.lb = tk.Listbox(self.dropdown_parent, font=self.font, height=self.height)
                
                self.lb.bind("<Double-Button-1>", self.selection)
                self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                self.lb_up = True
            
            self.lb.delete(0, tk.END)
            for w in words:
                self.lb.insert(tk.END,w)
        else:
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        
    def selection(self, _):
        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def up(self, _):
        if self.lb_up and not self.lb.curselection() == ():
            index = self.lb.curselection()[0]
            if index >= 0:
                self.lb.yview_scroll(-1, "units")
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, _):
        if self.lb_up:
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
