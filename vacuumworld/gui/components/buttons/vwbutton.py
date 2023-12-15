from typing import Callable, Literal
from PIL.ImageTk import PhotoImage
from PIL.Image import Image as PILImage
from tkinter import Button, Frame
from typing import Any, cast

from pystarworldsturbo.utils.json.json_value import JSONValue

from .vwtooltips import create_tooltip


class VWButton():
    '''
    This class is a wrapper around `Button` that specifies the buttons for the VacuumWorld GUI.

    A `VWButton` has a text, an image, a function to be executed when it is clicked and a tooltip text.
    '''
    def __init__(self, parent: Frame, config: dict[str, JSONValue], img: PILImage, fun: Callable[..., Any], text: str="", tip_text: str="") -> None:
        self.__img: PhotoImage = PhotoImage(img)
        self.__fun: Callable[..., Any] = fun
        self.__button: Button = Button(parent, text=text, bd=0, font=cast(list[str | int], config["root_font"]), fg=cast(str, config["buttons_fg_colour"]), highlightthickness=0, bg=cast(str, config["bg_colour"]), activebackground=cast(str, config["bg_colour"]), activeforeground=cast(str, config["bg_colour"]), highlightcolor=cast(str, config["bg_colour"]), compound="center", command=self.__fun)
        self.__button.config(image=self.__img)
        self.__tooltip_enabled: bool = cast(bool, config["tooltips"])
        self.__tip_text: str = tip_text

        if self.__tooltip_enabled and self.__tip_text:
            create_tooltip(widget=self.__button, text=self.__tip_text, config=config)

    def pack(self, side: Literal["left", "right", "top", "bottom"]) -> None:
        '''
        Packs the wrapped `Button` into the parent `Frame`, according to the provided `side`.
        '''
        self.__button.pack(side=side)

    def get_button(self) -> Button:
        '''
        Returns the proper `Button` object that this class wraps.
        '''
        return self.__button

    def set_img(self, img: PhotoImage) -> None:
        '''
        Sets the image of the wrapped `Button` to the provided `PhotoImage`.
        '''
        self.__img = img

    def get_img(self) -> PhotoImage:
        '''
        Returns the `PhotoImage` of the wrapped `Button`.
        '''
        return self.__img
