from typing import Callable, List
from PIL import Image
from PIL.ImageTk import PhotoImage
from tkinter import Frame, Image as Img

from .vwbutton import VWButton



class VWDifficultyButton(VWButton):
    def __init__(self, parent: Frame, config: dict, img: Img, fun: Callable, tip_text: str) -> None:
        self.__imgs: List[PhotoImage] = [PhotoImage(img)]
        self.__imgs.extend([VWDifficultyButton.next_image(img, i * (255/(len(config["user_mind_levels"])-1))) for i in range(1, len(config["user_mind_levels"]))])
        super(VWDifficultyButton, self).__init__(parent=parent, config=config, img=img, fun=self.onclick, tip_text=tip_text)
        self.__difficulty: int = config["default_user_mind_level"]
        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())
        self._rfun: Callable = fun

    @staticmethod
    def next_image(img, red) -> PhotoImage:
        img_dif: Image.Image = Image.new("RGB", img.size)
        img_dif.paste(img)
        rr, gg, bb = img_dif.split()
        rr = rr.point(lambda p: p + red)
        img_dif: Image.Image = Image.merge("RGB", (rr, gg, bb))

        return PhotoImage(img_dif)

    def get_difficulty(self) -> int:
        return self.__difficulty

    def onclick(self) -> None:
        self.__difficulty = (self.__difficulty + 1) % len(self.__imgs)
        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())
        self._rfun()
