from tkinter import Entry, Frame, StringVar, Listbox, END, ACTIVE
from re import match
from typing import List
from pyoptional.pyoptional import PyOptional


# Inspired by https://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
class VWAutocompleteEntry(Entry):
    '''
    This class specifies an `Entry` with autocomplete functionality.
    '''
    def __init__(self, lista: List[str], height: int, *args, **kwargs) -> None:
        super(VWAutocompleteEntry, self).__init__(*args, **kwargs)

        self.__dropdown_parent: Frame = args[0]
        self.__lista: List[str] = lista
        self.__var: StringVar = self["textvariable"] if "textvariable" in kwargs else StringVar()
        self.__font: tuple = kwargs.get("font", None)

        self.__var.trace("w", self.__changed)

        self.__height: int = int(height)

        self.bind("<Right>", self.__selection)
        self.bind("<Return>", self.__selection)
        self.bind("<Up>", self.__up)
        self.bind("<Down>", self.__down)

        self.__lb: PyOptional[Listbox] = PyOptional.empty()
        self.__lb_up: bool = False

    def set_list_a(self, list_a: List[str]) -> None:
        '''
        Sets the list of words to be used for autocomplete from the `list_a` argument.

        This method assumes (via assertions) that the `list_a` argument is a `List[str]`.
        '''
        assert isinstance(list_a, list)
        assert all(isinstance(x, str) for x in list_a)

        self.__lista = list_a

    def get_var(self) -> StringVar:
        '''
        Returns the `StringVar` object associated with this `VWAutocompleteEntry` object.
        '''
        return self.__var

    def __changed(self, *_) -> None:
        if self.__var.get() == "":
            self.__lb.if_present(lambda x: x.destroy())

            self.__lb_up = False
        else:
            self.__check_words()

    def __check_words(self) -> None:
        words = self.__comparison()

        if words:
            if not self.__lb_up:
                self.__lb = PyOptional.of(Listbox(self.__dropdown_parent, font=self.__font, height=self.__height))

                self.__lb.or_else_raise().bind("<Double-Button-1>", self.__selection)
                self.__lb.or_else_raise().place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())

                self.__lb_up = True

            self.__lb.or_else_raise().delete(0, END)

            for w in words:
                self.__lb.or_else_raise().insert(END, w)
        elif self.__lb_up:
            self.__lb.or_else_raise().destroy()

            self.__lb_up = False

    def __selection(self, _) -> None:
        if self.__lb_up:
            self.__var.set(self.__lb.or_else_raise().get(ACTIVE))
            self.__lb.or_else_raise().destroy()

            self.__lb_up = False

            self.icursor(END)

    def __up(self, _) -> None:
        if self.__lb_up and self.__lb.or_else_raise().curselection() != ():
            index: int = self.__lb.or_else_raise().curselection()[0]

            if index >= 0:
                self.__lb.or_else_raise().yview_scroll(-1, "units")
                self.__lb.or_else_raise().selection_clear(first=index)

                index_str: str = str(int(index)-1)

                self.__lb.or_else_raise().selection_set(first=index_str)
                self.__lb.or_else_raise().activate(index_str)

    def __down(self, _) -> None:
        if self.__lb_up:
            if self.__lb.or_else_raise().curselection() == ():
                self.__lb.or_else_raise().selection_set(first=0)
                self.__lb.or_else_raise().activate(0)

                return

            index: int = self.__lb.or_else_raise().curselection()[0]

            if int(index) + 1 < len(self.__lista):
                if int(index) + 1 >= self.__height:
                    self.__lb.or_else_raise().yview_scroll(1, "units")

                self.__lb.or_else_raise().selection_clear(first=index)

                index_str: str = str(int(index)+1)

                self.__lb.or_else_raise().selection_set(first=index_str)
                self.__lb.or_else_raise().activate(index_str)

    def __comparison(self) -> List[str]:
        return [w for w in self.__lista if match(".*" + self.__var.get() + ".*", w)]
