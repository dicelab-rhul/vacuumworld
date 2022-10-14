"""
CREDIT: http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
"""

from tkinter import Entry, Frame, StringVar, Listbox, END, ACTIVE
from re import match
from typing import List



class AutocompleteEntry(Entry):
    def __init__(self, lista: List[str], height: int, *args, **kwargs) -> None:
        Entry.__init__(self, *args, **kwargs)
        self.dropdown_parent: Frame = args[0]
        self.lista: List[str] = lista
        self.var: StringVar = self["textvariable"]
        self.font: tuple = kwargs.get("font", None)
        if self.var == "":
            self.var = self["textvariable"] = StringVar()
        self.var.trace("w", self.__changed)
        self.height: int = int(height)
        self.bind("<Right>", self.__selection)
        self.bind("<Return>", self.__selection)
        self.bind("<Up>", self.__up)
        self.bind("<Down>", self.__down)
        self.lb: Listbox = None
        self.lb_up: bool = False

    def __changed(self, *_) -> None:
        if self.var.get() == "":
            if self.lb:
                self.lb.destroy()
            self.lb_up = False
        else:
            self.__check_words()

    def __check_words(self) -> None:
        words = self.__comparison()
        if words:
            if not self.lb_up:
                self.lb = Listbox(self.dropdown_parent, font=self.font, height=self.height)

                self.lb.bind("<Double-Button-1>", self.__selection)
                self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                self.lb_up = True

            self.lb.delete(0, END)
            for w in words:
                self.lb.insert(END, w)
        else:
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False

    def __selection(self, _) -> None:
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def __up(self, _) -> None:
        if self.lb_up and self.lb.curselection() != ():
            index: int = self.lb.curselection()[0]
            if index >= 0:
                self.lb.yview_scroll(-1, "units")
                self.lb.selection_clear(first=index)
                index_str: str = str(int(index)-1)
                self.lb.selection_set(first=index_str)
                self.lb.activate(index_str)

    def __down(self, _) -> None:
        if self.lb_up:
            if self.lb.curselection() == ():
                self.lb.selection_set(first=0)
                self.lb.activate(0)
                return

            index: int = self.lb.curselection()[0]
            if int(index) + 1 < len(self.lista):
                if int(index) + 1 >= self.height:
                    self.lb.yview_scroll(1, "units")

                self.lb.selection_clear(first=index)
                index_str: str = str(int(index)+1)
                self.lb.selection_set(first=index_str)
                self.lb.activate(index_str)

    def __comparison(self) -> List[str]:
        return [w for w in self.lista if match(".*" + self.var.get() + ".*", w)]
