from tkinter import Button, Label, Toplevel, LEFT, SOLID
from typing import cast
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.utils.json.json_value import JSONValue


class VWToolTip():
    '''
    This class is used to create tooltips for each `VWButton`.
    '''
    def __init__(self, widget: Button, config: dict[str, JSONValue]) -> None:
        self.__widget: Button = widget
        self.__config: dict[str, JSONValue] = config
        self.__already_init: bool = False

    def showtip(self, text: str) -> None:
        '''
        This method is used to show the tooltip.

        It needs to be bound to some event, like `<Enter>` or `<Leave>`.
        '''
        self.__text: str = text

        if not self.__already_init:
            self.__tipwindow: PyOptional[Toplevel] = PyOptional[Toplevel].empty()
            self.__already_init = True

        if self.__tipwindow.is_present() or not self.__text:
            return

        bbox: tuple[int, int, int, int] | None = self.__widget.bbox()
        x, y, _, cy = bbox if bbox else (0, 0, 0, 0)
        x: int = x + self.__widget.winfo_rootx() + 57
        y: int = y + cy + self.__widget.winfo_rooty() + 27
        tw = Toplevel(self.__widget)

        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        self.__tipwindow = PyOptional[Toplevel].of(tw)

        label: Label = Label(tw, text=self.__text, justify=LEFT, bg=cast(str, self.__config["tooltips_bg_colour"]), relief=SOLID, borderwidth=1, font=cast(list[str | int], self.__config["tooltips_font"]), fg=cast(str, self.__config["tooltips_fg_colour"]))
        label.pack(ipadx=1)

    def hidetip(self) -> None:
        '''
        This method is used to hide the tooltip.

        It needs to be bound to some event, like `<Enter>` or `<Leave>`.
        '''
        if self.__tipwindow.is_present():
            tw: Toplevel = self.__tipwindow.or_else_raise()

            tw.destroy()

        self.__tipwindow = PyOptional[Toplevel].empty()


def create_tooltip(widget: Button, text: str, config: dict[str, JSONValue]) -> None:
    '''
    Creates the tooltip for the given `widget` with the given `text`.

    It also binds the `showtip()` and `hidetip()` methods to the `<Enter>` and `<Leave>` events.
    '''
    tooltip: VWToolTip = VWToolTip(widget=widget, config=config)

    widget.bind("<Enter>", lambda _: tooltip.showtip(text))
    widget.bind("<Leave>", lambda _: tooltip.hidetip())
