# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
@author: cloudstrife9999
"""

import os
import pickle
import traceback

from ..core.environment.vw import Grid

from re import match
from random import choice
from string import ascii_letters
from tkinter.filedialog import asksaveasfile, askopenfile
from typing import List



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

    def save_state(self, grid: Grid, file: str) -> bool:
        assert grid

        if file and not self.__file_exists(file) and match(self.__vw_file_regex, file):
            return self.__quick_save(grid, file)
        else:
            return self.__save_dialog(grid, file)

    def __quick_save(self, grid: Grid, file: str) -> bool:
        assert file

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(file)), "wb") as f:
                pickle.dump(grid, f)
                return True
        except Exception:
            traceback.print_exc()
            return False

    def __save_dialog(self, grid: Grid, file: str) -> bool:
        try:
            if not file:
                file = "".join(choice(ascii_letters) for _ in range(self.__random_file_name_length)) + self.__vw_extension
            elif not file.endswith(self.__vw_extension):
                file += self.__vw_extension

            with asksaveasfile(mode="wb", initialdir=self.__files_dir, initialfile=file, defaultextension=self.__vw_extension) as f:
                pickle.dump(grid, f)
                return True
        except AttributeError:
            return False
        except Exception:
            traceback.print_exc()
            return False

    def load_state(self, file: str="") -> Grid:
        if file and self.__file_exists(file) and match(self.__vw_file_regex, file):
            return self.__quick_load(file)
        else:
            return self.__load_dialog(file)

    def __quick_load(self, file: str) -> Grid:
        assert file

        try:
            with open(os.path.join(self.__files_dir, os.path.basename(file)), "rb") as f:
                return pickle.load(f)
        except Exception:
            traceback.print_exc()
            return None

    def __load_dialog(self, file: str="") -> Grid:
        try:
            with askopenfile(mode="rb", initialdir=self.__files_dir, initialfile=file) as f:
                return pickle.load(f)
        except AttributeError:
            return None
        except Exception:
            traceback.print_exc()
            return None
    
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
            traceback.print_exc()
            return []
