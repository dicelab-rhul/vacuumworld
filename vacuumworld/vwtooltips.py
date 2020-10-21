
from tkinter import Label, Toplevel, LEFT, SOLID

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text

        if self.tipwindow or not self.text:
            return

        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT, bg="#ffffe0", relief=SOLID, borderwidth=1, font=("tahoma", "8", "normal"), fg="#000000")
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None

        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tooltip = ToolTip(widget)

    def enter(_):
        tooltip.showtip(text)

    def leave(_):
        tooltip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
