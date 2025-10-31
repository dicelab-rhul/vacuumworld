from tkinter import Canvas, Event
from typing import Callable, cast
from PIL.ImageTk import PhotoImage

from pystarworldsturbo.utils.json.json_value import JSONValue

from .vwbounds_manager import VWBoundsManager


class VWCanvasDragManager():
    '''
    This class speficies the behaviour of a drag manager for a `Canvas` object.
    '''
    def __init__(self, config: dict[str, JSONValue], key: tuple[str, str], grid_dim: int, canvas: Canvas, item: int, on_start_callback: Callable[..., None], on_drop_callback: Callable[..., None]) -> None:
        self.__config: dict[str, JSONValue] = config
        self.__bounds_manager: VWBoundsManager = VWBoundsManager(config=config)

        self.__x: float = 0.0
        self.__y: float = 0.0

        self.__grid_dim: int = grid_dim
        self.__canvas: Canvas = canvas

        self.__on_start_callback: Callable[..., None] = on_start_callback
        self.__on_drop_callback: Callable[..., None] = on_drop_callback
        self.__canvas.tag_bind(item, "<ButtonPress-1>", self.on_start)
        self.__canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.__canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drop)

        self.__key: tuple[str, str] = key
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
        Move the image while dragging, aligned to the correct float-based grid.
        '''
        grid_size: int = cast(int, self.__config["grid_size"])
        inc: float = grid_size / self.__grid_dim
        env_dim: int = self.__grid_dim
        x_index: int = min(int(event.x // inc), env_dim - 1)
        y_index: int = min(int(event.y // inc), env_dim - 1)

        # Center of the target cell
        x: float = x_index * inc + inc / 2
        y: float = y_index * inc + inc / 2

        # Check bounds based on raw cursor position, not snapped center
        if not self.__bounds_manager.in_bounds(x=event.x, y=event.y):
            self.__canvas.itemconfigure(self.__drag, state="hidden")

            return
        else:
            self.__canvas.itemconfigure(self.__drag, state="normal")

        # Only move if actually changed
        if x != self.__x or y != self.__y:
            dx = x - self.__x
            dy = y - self.__y
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

    def get_key(self) -> tuple[str, str]:
        '''
        Returns the key of the `Image` objectas a `tuple[str, str]`.
        '''
        return self.__key

    def get_drag(self) -> int:
        '''
        Returns the `int` index of the image to be dragged.
        '''
        return self.__drag

    def set_drag(self, drag: int) -> None:
        '''
        Sets the index of the image to be dragged as an `int`.
        '''
        self.__drag: int = drag

    def get_drag_image(self) -> PhotoImage:
        '''
        Returns the `PhotoImage` object to be dragged as a `PhotoImage`.
        '''
        return self.__drag_image

    def set_drag_image(self, drag_image: PhotoImage) -> None:
        '''
        Sets the `Image` object to be dragged as a `PhotoImage`.
        '''
        self.__drag_image: PhotoImage = drag_image
