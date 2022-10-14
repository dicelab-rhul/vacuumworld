from tkinter import Tk, Frame, Canvas, Image as Img
from typing import Callable, Dict
from PIL import Image
from PIL.ImageTk import PhotoImage

from ..buttons.vwbutton import VWButton
from ....model.environment.vwenvironment import VWEnvironment

import os



class VWInitialWindow(Frame):
    def __init__(self, parent: Tk, config: dict, buttons: dict, env: VWEnvironment, _start: Callable, _exit: Callable, _guide: Callable) -> None:
        super(VWInitialWindow, self).__init__(parent)

        self.__config: dict = config
        self.__button_data: dict = buttons

        self.__button_data["start"]["action"] = lambda: _start(env)
        self.__button_data["guide"]["action"] = _guide
        self.__button_data["exit"]["action"] = _exit

        self.configure(background=self.__config["bg_colour"])
        self.__canvas: Canvas = Canvas(self, width=self.__config["grid_size"]+1, height=self.__config["grid_size"]+1, bd=0, highlightthickness=0)

        self.__img_tk: PhotoImage = PhotoImage(Image.open(self.__config["main_menu_image_path"]).resize((int(self.__config["grid_size"]), int(self.__config["grid_size"])), Image.BICUBIC))
        self.__image: Img = self.__canvas.create_image(self.__config["grid_size"]/2, self.__config["grid_size"]/2, image=self.__img_tk)

        self.__button_frame: Frame = Frame(self)

        self.__canvas.pack()
        self.__buttons: Dict[str, VWButton] = {}

        for button_name in ("start", "guide", "exit"):
            self.__buttons[button_name] = self.__build_button(button_name=button_name, parent=self.__button_frame)
            self.__buttons[button_name].pack("left")

        self.__button_frame.pack()

        # Note: pack() for VWInitialWindow needs to be called by the caller.

    def get_image(self) -> Img:
        return self.__image

    def __build_button(self, button_name: str, parent: Frame) -> VWButton:
        action: Callable = self.__button_data[button_name]["action"]
        text: str = self.__button_data[button_name]["text"]
        image: Img = Image.open(os.path.join(self.__config["button_data_path"], self.__button_data[button_name]["image_file"]))
        image = image.resize((int(image.width), int(image.height)), Image.BICUBIC)
        tip_text: str = self.__button_data[button_name]["tip_text"]

        return VWButton(parent=parent, config=self.__config, img=image, fun=action, text=text, tip_text=tip_text)
