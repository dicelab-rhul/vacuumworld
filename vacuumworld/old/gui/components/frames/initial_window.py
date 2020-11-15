from tkinter import Tk, Frame, Canvas, Image as Img
from typing import Callable, Dict
from PIL import ImageTk, Image

from ..buttons.vwbutton import VWButton

import os



class VWInitialWindow(Frame):
    def __init__(self, root: Tk, config: dict, _start: Callable, _exit: Callable, _guide: Callable) -> None:
        super(VWInitialWindow,self).__init__(root)
        
        self.__config: dict = config
        
        self.configure(background=self.__config["bg_colour"])
        self.__canvas: Canvas = Canvas(self, width = self.__config["grid_size"] + 1, height = self.__config["grid_size"] + 1, bd=0, highlightthickness=0)

        self.__img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(self.__config["main_menu_image_path"]).resize((int(self.__config["grid_size"]), int(self.__config["grid_size"])), Image.BICUBIC))
        self.__image: Img = self.__canvas.create_image(self.__config["grid_size"]/2,self.__config["grid_size"]/2,image=self.__img_tk)
        
        self.__button_frame: Frame = Frame(self)

        self.__canvas.pack()
        self.__buttons: Dict[str, VWButton] = {}

        button_image: Img = Image.open(os.path.join(self.__config["button_images_path"], "button.png"))
        button_image = button_image.resize((int(button_image.width), int(button_image.height)), Image.BICUBIC)


        self.__buttons["start"] = VWButton(self.__button_frame, self.__config, button_image, _start, text="Start", tip_text="Click here to set-up the simulation.")
        self.__buttons["exit"] = VWButton(self.__button_frame, self.__config, button_image, _exit, text="Exit", tip_text="Click here to exit VacuumWorld.")
        self.__buttons["guide"] = VWButton(self.__button_frame, self.__config, button_image, _guide, text="Guide", tip_text="Click here to open the project's GitHub page.")
        
        self.__buttons["start"].pack("left")
        self.__buttons["guide"].pack("left")
        self.__buttons["exit"].pack("left")
        self.__button_frame.pack()

        # Note: pack() needs to be called by the caller.
    
    def get_image(self) -> Img:
        return self.__image
