from .vwbutton import VWButton
from ....core.user.vwuser import DIFFICULTY_LEVELS

from PIL import ImageTk, Image



class VWDifficultyButton(VWButton):
    def __init__(self, root, config, img, fun, tip_text):
        self.__imgs = [ImageTk.PhotoImage(img)]
        self.__imgs.extend([VWDifficultyButton.next_image(img, i * (255/(DIFFICULTY_LEVELS-1))) for i in range(1, DIFFICULTY_LEVELS)])
        super(VWDifficultyButton, self).__init__(root=root, config=config, img=img, fun=self.onclick, tip_text=tip_text)
        self.__difficulty = config["default_user_mind_level"]
        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())
        self._rfun = fun

    @staticmethod
    def next_image(img, red):
        img_dif = Image.new("RGB", img.size)
        img_dif.paste(img)
        rr, gg, bb = img_dif.split()
        rr = rr.point(lambda p: p + red)
        img_dif = Image.merge("RGB", (rr, gg, bb))
        return ImageTk.PhotoImage(img_dif)

    def get_difficulty(self) -> int:
        return self.__difficulty

    def onclick(self):
        self.__difficulty = (self.__difficulty + 1) % len(self.__imgs)
        self.set_img(self.__imgs[self.__difficulty])
        self.get_button().config(image=self.get_img())
        self._rfun()
