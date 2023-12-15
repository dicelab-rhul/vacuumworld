from json import load, dump
from re import match
from random import choice
from string import ascii_letters
from tkinter.filedialog import asksaveasfile, askopenfile
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.utils.json.json_value import JSONValue

from ..model.environment.vwenvironment import VWEnvironment

import os


class VWSaveStateManager():
    '''
    This class is responsible for saving and loading the state of a `VWEnvironment`.

    It supports saving and loading to and from a file, both with a saveload dialog and without it.

    The format of the saved states is JSON.
    '''
    def __init__(self) -> None:
        self.__files_dir: str = os.path.join(os.getcwd(), "files")
        self.__vw_saved_state_extension: str = ".json"
        self.__vw_file_regex: str = f"^[a-zA-Z0-9]+{self.__vw_saved_state_extension}$"
        self.__random_file_name_length: int = 10

        self.__prepare_files_dir()

    def get_vw_saved_state_extension(self) -> str:
        '''
        Returns the extension of the saved states.
        '''
        return self.__vw_saved_state_extension

    def __prepare_files_dir(self) -> None:
        if not os.path.exists(self.__files_dir):
            os.mkdir(self.__files_dir)
        elif not os.path.isdir(self.__files_dir):
            raise IOError(f"Could not create the `{self.__files_dir}` directory, because something with the same name that is not a directory already exists.")

        if not os.path.isdir(self.__files_dir):  # The directory was not created.
            raise IOError(f"Could not create the `{self.__files_dir}` directory.")

    def __file_exists(self, filename: str) -> bool:
        assert filename and isinstance(filename, str)

        # Absolute path vs. relative path.
        return os.path.exists(filename) or os.path.exists(os.path.join(self.__files_dir, os.path.basename(filename)))

    def save_state(self, env: VWEnvironment, filename: str) -> bool:
        '''
        Saves the state of the given `VWEnvironment` to a file.

        It supports saving to a file both with a saveload dialog and without it.
        '''
        assert env

        state: dict[str, JSONValue] = env.to_json()

        if filename and not self.__file_exists(filename) and match(self.__vw_file_regex, filename):
            return self.__quick_save(state=state, filename=filename)
        else:
            return self.__save_dialog(state=state, filename=filename)

    def __quick_save(self, state: dict[str, JSONValue], filename: str) -> bool:
        assert filename

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(filename)), "w") as f:
                dump(obj=state, fp=f, indent=4)
                return True
        except Exception:
            return False

    def __save_dialog(self, state: dict[str, JSONValue], filename: str) -> bool:
        try:
            if not filename:
                filename = "".join(choice(ascii_letters) for _ in range(self.__random_file_name_length)) + self.__vw_saved_state_extension
            elif not filename.endswith(self.__vw_saved_state_extension):
                filename += self.__vw_saved_state_extension

            with PyOptional.of_nullable(asksaveasfile(mode="w", initialdir=self.__files_dir, initialfile=filename, defaultextension=self.__vw_saved_state_extension)).or_else_raise() as f:
                dump(obj=state, fp=f, indent=4)
                return True
        except AttributeError:
            return False
        except Exception:
            return False

    def load_state(self, filename: str="", no_gui: bool=False) -> dict[str, JSONValue]:
        '''
        Loads the state of a `VWEnvironment` from a file.

        It supports loading from a file both with a saveload dialog and without it.
        '''
        if filename and self.__file_exists(filename) and match(self.__vw_file_regex, os.path.basename(filename)):
            return self.__quick_load(filename)
        elif no_gui:
            return {}
        else:
            return self.__load_dialog(filename)

    def __quick_load(self, filename: str) -> dict[str, JSONValue]:
        assert filename

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(filename)), "rb") as f:
                return load(fp=f)
        except Exception:
            return {}

    def __load_dialog(self, file: str="") -> dict[str, JSONValue]:
        try:
            with PyOptional.of_nullable(askopenfile(mode="rb", initialdir=self.__files_dir, initialfile=file)).or_else_raise() as f:
                return load(fp=f)
        except AttributeError:
            return {}
        except Exception:
            return {}

    def add_vw_extension_to_filename_string_if_missing(self, filename: str) -> str:
        '''
        Amends the given `filename` `str` with the extension of the saved states if it is missing, then returns the amented `str`.
        '''
        assert filename

        if not filename.endswith(self.__vw_saved_state_extension):
            filename += self.__vw_saved_state_extension
        return filename

    def get_ordered_list_of_filenames_in_save_directory(self) -> list[str]:
        '''
        Returns a `list[str]` of the filenames in the save directory, sorted in ascending order.

        If an error occurs, an empty `list` is returned.
        '''
        try:
            f: list[str] = [file for file in os.listdir(self.__files_dir) if file.endswith(self.__vw_saved_state_extension)]

            f.sort()

            return f
        except Exception:
            return []

    def remove_saved_state(self, filename: str) -> None:
        '''
        Removes the saved state with the given `filename` from the save directory.

        If an error occurs, nothing happens.
        '''
        assert self.__file_exists(os.path.join(self.__files_dir, os.path.basename(filename))) and match(self.__vw_file_regex, os.path.basename(filename))

        try:
            os.remove(os.path.join(self.__files_dir, os.path.basename(filename)))
        except Exception:
            pass
