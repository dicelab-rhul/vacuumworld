from json import load, dump
from re import match
from random import choice
from string import ascii_letters
from tkinter.filedialog import asksaveasfile, askopenfile
from typing import List

from ..model.environment.vwenvironment import VWEnvironment

import os



class SaveStateManager():
    def __init__(self) -> None:
        self.__files_dir: str = os.path.join(os.getcwd(), "files")
        self.__vw_extension: str = ".vw"
        self.__vw_file_regex: str = "^[a-zA-Z0-9]+{}$".format(self.__vw_extension)
        self.__random_file_name_length: int = 10

        self.__prepare_files_dir()

    def __prepare_files_dir(self) -> None:
        if not os.path.exists(self.__files_dir):
            os.mkdir(self.__files_dir)
        elif not os.path.isdir(self.__files_dir):
            raise ValueError("Could not create the `{}` directory.".format(self.__files_dir))

        if not os.path.isdir(self.__files_dir): # the directory was not created
            raise ValueError("Could not create the `{}` directory.".format(self.__files_dir))

    def __file_exists(self, file: str) -> bool:
        assert file and type(file) == str

        # Absolute path vs. relative path
        return os.path.exists(file) or os.path.exists(os.path.join(self.__files_dir, os.path.basename(file)))

    def save_state(self, env: VWEnvironment, file: str) -> bool:
        assert env

        state: dict = env.to_json()

        if file and not self.__file_exists(file) and match(self.__vw_file_regex, file):
            return self.__quick_save(state=state, file=file)
        else:
            return self.__save_dialog(state=state, file=file)

    def __quick_save(self, state: dict, file: str) -> bool:
        assert file

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(file)), "wb") as f:
                dump(obj=state, fp=f, indent=4)
                return True
        except Exception:
            return False

    def __save_dialog(self, state: dict, file: str) -> bool:
        try:
            if not file:
                file = "".join(choice(ascii_letters) for _ in range(self.__random_file_name_length)) + self.__vw_extension
            elif not file.endswith(self.__vw_extension):
                file += self.__vw_extension

            with asksaveasfile(mode="w", initialdir=self.__files_dir, initialfile=file, defaultextension=self.__vw_extension) as f:
                dump(obj=state, fp=f, indent=4)
                return True
        except AttributeError:
            return False
        except Exception:
            return False

    def load_state(self, file: str="") -> dict:
        if file and self.__file_exists(file) and match(self.__vw_file_regex, file):
            return self.__quick_load(file)
        else:
            return self.__load_dialog(file)

    def __quick_load(self, file: str) -> dict:
        assert file

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(file)), "rb") as f:
                return load(fp=f)
        except Exception:
            return {}

    def __load_dialog(self, file: str="") -> dict:
        try:
            with askopenfile(mode="rb", initialdir=self.__files_dir, initialfile=file) as f:
                return load(fp=f)
        except AttributeError:
            return {}
        except Exception:
            return {}
    
    def add_vw_extension_to_filename_string_if_missing(self, file: str) -> str:
        assert file

        if not file.endswith(self.__vw_extension):
            file += self.__vw_extension
        return file

    def get_ordered_list_of_filenames_in_save_directory(self) -> List[str]:
        try:
            f: List[str] = [file for file in os.listdir(self.__files_dir) if file.endswith(self.__vw_extension)]
            f.sort()
            return f
        except Exception:
            return []
