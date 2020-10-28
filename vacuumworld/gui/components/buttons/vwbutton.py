from typing import Callable
from PIL import ImageTk
from tkinter import Button, Frame, Image

from .vwtooltips import create_tooltip



class VWButton():
    def __init__(self, root: Frame, config: dict, img: Image, fun, text: str=None, tip_text: str="") -> None:
        self.__img: ImageTk.PhotoImage = ImageTk.PhotoImage(img)
        self.__fun: Callable = fun
        self.__button: Button = Button(root, text = text, bd=0, font = config["root_font"], fg=config["buttons_fg_colour"],
                                 highlightthickness = 0, bg=config["bg_colour"], activebackground=config["bg_colour"],
                                 activeforeground=config["bg_colour"], highlightcolor=config["bg_colour"], compound = "center",
                                 command = self.__fun)
        self.__button.config(image=self.__img)
        self.__tooltip_enabled: bool = config["tooltips"]
        self.__tip_text: str = tip_text

        if self.__tooltip_enabled and self.__tip_text:
            create_tooltip(widget=self.__button, text=self.__tip_text, config=config)

    def pack(self, side: str) -> None:
        self.__button.pack(side=side)
        
    def grid(self, row: int, col: int) -> None:
        self.__button.grid(row=row,column=col)
        
    def destroy(self) -> None:
        self.__button.destroy()
        self.__img.destroy()

    def get_button(self) -> Button:
        return self.__button

    def set_img(self, img: ImageTk.PhotoImage) -> None:
        self.__img = img

    def get_img(self) -> ImageTk.PhotoImage:
        return self.__img
