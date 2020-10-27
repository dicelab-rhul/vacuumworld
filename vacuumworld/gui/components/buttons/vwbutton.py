from PIL import ImageTk
from tkinter import Button

from .vwtooltips import create_tooltip



class VWButton():
    def __init__(self, root, config, img, fun, text:str=None, tooltip: bool=False, tip_text=""):
        self.__img = ImageTk.PhotoImage(img)
        self.__fun: callable = fun
        self.__button: Button = Button(root, text = text, bd=0, font = config["root_font"], fg=config["buttons_fg_colour"],
                                 highlightthickness = 0, bg=config["bg_colour"], activebackground=config["bg_colour"],
                                 activeforeground=config["bg_colour"], highlightcolor=config["bg_colour"], compound = "center",
                                 command = self.__fun)
        self.__button.config(image=self.__img)
        self.__tooltip_enabled: bool = tooltip
        self.__tip_text = tip_text

        if self.__tooltip_enabled and self.__tip_text:
            create_tooltip(widget=self.__button, text=self.__tip_text)

    def pack(self, side):
        self.__button.pack(side=side)
        
    def grid(self, row, col):
        self.__button.grid(row=row,column=col)
        
    def destroy(self):
        self.__button.destroy()
        self.__img.destroy()

    def get_button(self) -> Button:
        return self.__button

    def set_img(self, img) -> None:
        self.__img = img

    def get_img(self):
        return self.__img
