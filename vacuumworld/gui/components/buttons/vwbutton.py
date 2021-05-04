from typing import Callable
from PIL.ImageTk import PhotoImage
from tkinter import Button, Frame, Image

from .vwtooltips import create_tooltip



class VWButton():
    def __init__(self, parent: Frame, config: dict, img: Image, fun: Callable, text: str=None, tip_text: str="") -> None:
        self.__img: PhotoImage = PhotoImage(img)
        self.__fun: Callable = fun
        self.__button: Button = Button(parent, text = text, bd=0, font = config["root_font"], fg=config["buttons_fg_colour"],
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

    def get_button(self) -> Button:
        return self.__button

    def set_img(self, img: PhotoImage) -> None:
        self.__img = img

    def get_img(self) -> PhotoImage:
        return self.__img
