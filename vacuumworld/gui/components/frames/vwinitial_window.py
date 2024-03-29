from tkinter import Tk, Frame, Canvas
from typing import Callable, Any, cast
from PIL import Image
from PIL.Image import Image as PILImage
from PIL.ImageTk import PhotoImage

from pystarworldsturbo.utils.json.json_value import JSONValue

from ..buttons.vwbutton import VWButton
from ....model.environment.vwenvironment import VWEnvironment

import os


class VWInitialWindow(Frame):
    '''
    This class specifies the initial window that is displayed when VacuumWorld is started.

    The initial window contains a canvas with an image and three buttons: `start`, `guide` and `exit`:

    * `start` opens the simulation window.

    * `guide` opens the Wiki page in a new browser tab.

    * `exit` closes the application.
    '''
    def __init__(self, parent: Tk, config: dict[str, JSONValue], buttons: dict[str, JSONValue], env: VWEnvironment, _start: Callable[..., None], _exit: Callable[..., None], _guide: Callable[..., None]) -> None:
        super(VWInitialWindow, self).__init__(parent)

        self.__config: dict[str, JSONValue] = config
        # We need Any here, because we are adding lambda functions to the dict.
        self.__button_data: dict[str, Any] = buttons

        self.__button_data["start"]["action"] = lambda: _start(env)
        self.__button_data["guide"]["action"] = _guide
        self.__button_data["exit"]["action"] = _exit

        self.configure(background=cast(str, self.__config["bg_colour"]))
        self.__canvas: Canvas = Canvas(self, width=cast(int, self.__config["grid_size"]) + 1, height=cast(int, self.__config["grid_size"]) + 1, bd=0, highlightthickness=0)

        self.__img_tk: PhotoImage = PhotoImage(Image.open(cast(str, self.__config["main_menu_image_path"])).resize((int(cast(int, self.__config["grid_size"])), int(cast(int, self.__config["grid_size"]))), Image.BICUBIC))
        self.__image: int = self.__canvas.create_image(int(cast(int, self.__config["grid_size"]) / 2), int(cast(int, self.__config["grid_size"]) / 2), image=self.__img_tk)

        self.__button_frame: Frame = Frame(self)

        self.__canvas.pack()
        self.__buttons: dict[str, VWButton] = {}

        for button_name in ("start", "guide", "exit"):
            self.__buttons[button_name] = self.__build_button(button_name=button_name, parent=self.__button_frame)
            self.__buttons[button_name].pack("left")

        self.__button_frame.pack()

        # Note: pack() for VWInitialWindow needs to be called by the caller.

    def get_image(self) -> int:
        '''
        Returns the `int` ID of the image of the initial window.
        '''
        return self.__image

    def __build_button(self, button_name: str, parent: Frame) -> VWButton:
        action: Callable[..., None] = self.__button_data[button_name]["action"]
        text: str = self.__button_data[button_name]["text"]
        image: PILImage = Image.open(os.path.join(str(self.__config["button_data_path"]), str(self.__button_data[button_name]["image_file"])))
        image = image.resize((int(image.width), int(image.height)), Image.BICUBIC)
        tip_text: str = self.__button_data[button_name]["tip_text"]

        return VWButton(parent=parent, config=self.__config, img=image, fun=action, text=text, tip_text=tip_text)
