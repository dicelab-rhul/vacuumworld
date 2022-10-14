from tkinter import Button, Label, Toplevel, LEFT, SOLID


class ToolTip():
    def __init__(self, widget: Button, config: dict) -> None:
        self.__widget: Button = widget
        self.__config: dict = config
        self.__already_init: bool = False

    def showtip(self, text: str) -> None:
        self.__text: str = text

        if not self.__already_init:
            self.__tipwindow: Toplevel = None
            self.__already_init = True

        if self.__tipwindow or not self.__text:
            return

        x, y, _, cy = self.__widget.bbox("insert")
        x: int = x + self.__widget.winfo_rootx() + 57
        y: int = y + cy + self.__widget.winfo_rooty() + 27
        self.__tipwindow = tw = Toplevel(self.__widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label: Label = Label(tw, text=self.__text, justify=LEFT, bg=self.__config["tooltips_bg_colour"], relief=SOLID, borderwidth=1, font=self.__config["tooltips_font"], fg=self.__config["tooltips_fg_colour"])
        label.pack(ipadx=1)

    def hidetip(self) -> None:
        tw: Toplevel = self.__tipwindow
        self.__tipwindow = None

        if tw:
            tw.destroy()


def create_tooltip(widget: Button, text: str, config: dict) -> None:
    tooltip: ToolTip = ToolTip(widget=widget, config=config)

    widget.bind("<Enter>", lambda _: tooltip.showtip(text))
    widget.bind("<Leave>", lambda _: tooltip.hidetip())
