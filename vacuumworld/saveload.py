# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
@author: cloudstrife9999
"""

import os
import pickle
import traceback

from re import match
from random import choice
from string import ascii_letters
from tkinter.filedialog import asksaveasfile, askopenfile

#TODO: this should be a class, rather than a collection of methods and loose variables.

FILES_DIR = os.path.join(os.getcwd(), "files")
VW_EXTENSION = ".vw"
VW_FILE_REGEX = "^[a-zA-Z0-9]+{}$".format(VW_EXTENSION)
RANDOM_FILENAME_LENGTH = 10

def init():
    if not os.path.exists(FILES_DIR):
        os.mkdir(FILES_DIR)
    elif not os.path.isdir(FILES_DIR): # name collision
        raise ValueError("Could not create the `{}` directory.".format(FILES_DIR))

    if not os.path.isdir(FILES_DIR): # the directory was not created
        raise ValueError("Could not create the `{}` directory.".format(FILES_DIR))

def file_exists(file):
    assert file

    # Absolute path vs. relative path
    return os.path.exists(file) or os.path.exists(os.path.join(FILES_DIR, os.path.basename(file)))

def _save(grid, file):
    assert file

    try:
         with open(os.path.join(FILES_DIR, os.path.basename(file)), "wb") as f:
            pickle.dump(grid, f)
            return True
    except Exception:
        traceback.print_exc()
        return False

def save(grid, file):
    if file and not file_exists(file) and match(VW_FILE_REGEX, file):
        return _save(grid, file)
    else:
        return save_dialog(grid, file)

def save_dialog(grid, file):
    try:
        if not file:
            file = "".join(choice(ascii_letters) for _ in range(RANDOM_FILENAME_LENGTH)) + VW_EXTENSION
        elif not file.endswith(VW_EXTENSION):
            file += VW_EXTENSION

        with asksaveasfile(mode="wb", initialdir=FILES_DIR, initialfile=file, defaultextension=VW_EXTENSION) as f:
            pickle.dump(grid, f)
            return True
    except AttributeError:
        return False
    except Exception:
        traceback.print_exc()
        return False

def _load(file):
    assert file

    try:
        with open(os.path.join(FILES_DIR, os.path.basename(file)), "rb") as f:
            return pickle.load(f)
    except Exception:
        traceback.print_exc()
        return False

def load(file=""):
    if file and file_exists(file) and match(VW_FILE_REGEX, file):
        return _load(file)
    else:
        return load_dialog(file)

def load_dialog(file=""):
    try:
        with askopenfile(mode="rb", initialdir=FILES_DIR, initialfile=file) as f:
            return pickle.load(f)
    except AttributeError:
        return False
    except Exception:
        traceback.print_exc()
        return False
    
def add_vw_extension_to_filename_string_if_missing(file):
    assert file

    if not file.endswith(VW_EXTENSION):
        file += VW_EXTENSION
    return file

def get_ordered_list_of_filenames_in_save_directory():
    try:
        f = [file for file in os.listdir(FILES_DIR) if file.endswith(".vw")]
        f.sort()
        return f
    except Exception:
        traceback.print_exc()
        return []
