from typing import Callable
from PIL import Image
from PIL.ImageTk import PhotoImage
from PIL.Image import Image as PILImage
from tkinter import Frame
from typing import Any

from .vwbutton import VWButton


class VWDifficultyButton(VWButton):
    '''
    This class specifies the difficulty button that allows to dynamically switch between the `VWUserDifficulty` levels.

    It extends the `VWButton` class.
    '''
    def __init__(self, parent: Frame, config: dict[str, Any], img: PILImage, fun: Callable[..., None], tip_text: str) -> None:
        super(VWDifficultyButton, self).__init__(parent=parent, config=config, img=img, fun=self.onclick, tip_text=tip_text)

        self.__rfun: Callable[..., None] = fun
        self.__difficulty: int = config["default_user_mind_level"]
        self.__imgs: list[PhotoImage] = [PhotoImage(img)]

        self.__imgs.extend([VWDifficultyButton.next_image(img, i * (255/(len(config["user_mind_levels"])-1))) for i in range(1, len(config["user_mind_levels"]))])

        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())

    @staticmethod
    def next_image(img: PILImage, red: float) -> PhotoImage:
        '''
        Returns the appropriate `PhotoImage` for the selected `VWUserDifficulty`.
        '''
        img_dif: PILImage = Image.new("RGB", img.size)
        img_dif.paste(img)

        img_dif_channels: tuple[PILImage, ...] = img_dif.split()
        red_img: PILImage = Image.new("RGB", img.size, (int(red), 0, 0))
        img_dif: PILImage = Image.merge("RGB", (red_img.split()[0], img_dif_channels[1], img_dif_channels[2]))

        return PhotoImage(img_dif)

    def get_difficulty(self) -> int:
        '''
        Returns the selected `VWUserDifficulty` level as an `int`.
        '''
        return self.__difficulty

    def onclick(self) -> None:
        '''
        Specifies the behaviour of this `VWDifficultyButton` when it is clicked.
        '''
        self.__difficulty = (self.__difficulty + 1) % len(self.__imgs)

        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())

        self.__rfun()
