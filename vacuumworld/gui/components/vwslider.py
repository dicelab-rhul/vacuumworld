from tkinter import Canvas, Frame, Event, Image
from typing import Callable

from pystarworldsturbo.utils.utils import ignore


class VWSlider(Canvas):
    '''
    This class specifies a slider widget for the VacuumWorld GUI.
    '''
    def __init__(self, parent: Frame, config: dict, release_callback: Callable, slide_callback: Callable, width: float, height: float, increments: float=0, slider_width: float=8, start: float=0, **kwargs) -> None:
        super(VWSlider, self).__init__(parent, width=width, height=height, bd=0, highlightthickness=0, relief="ridge", bg=config["bg_colour"], **kwargs)

        self.__release_callback: Callable = release_callback
        self.__slide_callback: Callable = slide_callback

        self.__increments: float = increments
        self.__slide_item_dim: float = slider_width

        self.__x: float = start  # Real position of the slider.
        self.__inc: int = 0  # Incremental position of the slider [0-increments].

        if start > width:
            start = width - self.__slide_item_dim/2

        if increments:
            dx: int = int((width - self.__slide_item_dim) / self.__increments)
            self.__x = start * dx
            self.__inc = start

        self.background_item: Image = self.create_rectangle(0, 0, width-1, height-1, fill=config["bg_colour"])
        self.slider_item: Image = self.create_rectangle(self.__x, 0, self.__x + self.__slide_item_dim, height, fill=config["fg_colour"])

        self.bind("<ButtonPress-1>", self.on_start)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)

    def set_position(self, inc: int, callback: bool=True) -> None:
        '''
        Sets the position of the slider by moving it by `inc`.
        '''
        if inc != self.__inc:
            inc: int = max(0, min(inc, self.__increments))
            width: int = self.winfo_width() - self.__slide_item_dim
            old_x: float = self.__x

            self.__x = inc * int(width / self.__increments)
            self.__inc = inc

            self.move(self.slider_item, self.__x - old_x, 0)

            if callback:
                self.__slide_callback(self.__inc)
                self.__release_callback(self.__inc)

    def __move_slider(self, event: Event) -> None:
        width: int = self.winfo_width() - self.__slide_item_dim
        x: int = event.x

        if x > 0 and x < width:
            if self.__increments:
                inc: int = int(width / self.__increments)
                self.__inc = int(x / inc)
                x = self.__inc * inc

            dx: float = x - self.__x

            if dx != 0:
                self.move(self.slider_item, dx, 0)

                self.__slide_callback(self.__inc)

                self.__x = x

    def on_start(self, event: Event) -> None:
        '''
        This method is called when the user starts dragging the slider.

        Moves the slider to the position of the mouse.
        '''
        self.__move_slider(event)

    def on_drag(self, event: Event) -> None:
        '''
        This method is called when the user is dragging the slider.

        Keeps moving the slider to the position of the mouse.
        '''
        self.__move_slider(event)

    def on_drop(self, event: Event) -> None:
        '''
        This method is called when the user stops dragging the slider.

        Calls the release callback.
        '''
        ignore(event)

        x: float = self.__x

        if self.__increments:
            x = self.__inc

        self.__release_callback(int(x))
