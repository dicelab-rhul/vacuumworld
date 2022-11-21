from tkinter import Canvas, Event, Image
from typing import Callable, Tuple

from .vwbounds_manager import VWBoundsManager


class CanvasDragManager():
    '''
    This class speficies the behaviour of a drag manager for a `Canvas` object.
    '''
    def __init__(self, config: dict, key: Tuple[str, str], grid_dim: int, canvas: Canvas, item: Image, on_start_callback: Callable, on_drop_callback: Callable) -> None:
        self.__config: dict = config
        self.__bounds_manager: VWBoundsManager = VWBoundsManager(config=config)

        self.__x: int = 0
        self.__y: int = 0

        self.__grid_dim: int = grid_dim
        self.__canvas: Canvas = canvas

        self.__on_start_callback: Callable = on_start_callback
        self.__on_drop_callback: Callable = on_drop_callback
        self.__canvas.tag_bind(item, "<ButtonPress-1>", self.on_start)
        self.__canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.__canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drop)

        self.__key: Tuple[str, str] = key
        self.__drag_image: Image = None
        self.__drag: Image = None
        self.__dragging: bool = False

    def on_start(self, event: Event) -> None:
        '''
        This method is called when the user starts dragging the `Image` object.

        Starts the drag operation.
        '''
        if not self.__dragging:
            self.__on_start_callback(event)
            self.__dragging = True
            self.__x = event.x
            self.__y = event.y

    def on_drag(self, event: Event) -> None:
        '''
        This method is called when the user is dragging the `Image` object.

        Moves the `Image` object across the canvas.
        '''
        inc: int = self.__config["grid_size"] / self.__grid_dim
        x: int = int(event.x / inc) * inc + (inc / 2) + 1
        y: int = int(event.y / inc) * inc + (inc / 2) + 1

        if event.x < 0 or event.y < 0 or not self.__bounds_manager.in_bounds(x=x, y=y):
            self.__canvas.itemconfigure(self.__drag, state="hidden")
        elif x <= self.__config["grid_size"] and y <= self.__config["grid_size"] and self.__bounds_manager.in_bounds(x=x, y=y):
            self.__canvas.itemconfigure(self.__drag, state="normal")

        # To prevent unnecessary re-renderings.
        if x != self.__x or y != self.__y:
            dx: int = x - self.__x
            dy: int = y - self.__y
            self.__canvas.move(self.__drag, dx, dy)
            self.__x = x
            self.__y = y

    def on_drop(self, event: Event) -> None:
        '''
        This method is called when the user drops the `Image` object.

        Calls the proper on drop callback method if the `Image` has been dropped in bounds.
        '''
        if self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            self.__on_drop_callback(event, self)

        self.__dragging = False

    def get_key(self) -> Tuple[str, str]:
        '''
        Returns the key of the `Image` objectas a `Tuple[str, str]`.
        '''
        return self.__key

    def get_drag(self) -> Image:
        '''
        Returns the `_CanvasItemId` object to be dragged as an `Image`.
        '''
        return self.__drag

    def set_drag(self, drag: Image) -> None:
        '''
        Sets the `Image` object to be dragged as a `_CanvasItemId`.
        '''
        self.__drag = drag

    def get_drag_image(self) -> Image:
        '''
        Returns the `PhotoImage` object to be dragged as an `Image`.
        '''
        return self.__drag_image

    def set_drag_image(self, drag_image: Image) -> None:
        '''
        Sets the `Image` object to be dragged as a `PhotoImage`.
        '''
        self.__drag_image = drag_image
