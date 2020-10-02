#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
@author: cloudstrife9999
"""

import os
import pickle
import traceback

from random import choice
from string import ascii_letters
from tkinter.filedialog import asksaveasfile, askopenfile

FILES_DIR = os.path.join(os.getcwd(), "files")
VW_EXTENSION = ".vw"
RANDOM_FILENAME_LENGTH = 10

def init():
    if not os.path.isdir(FILES_DIR):
        os.mkdir(FILES_DIR)
    

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

def load_dialog(file):
    try:
        if not file:
            file = "".join(choice(ascii_letters) for _ in range(RANDOM_FILENAME_LENGTH)) + VW_EXTENSION
        elif not file.endswith(VW_EXTENSION):
            file += VW_EXTENSION

        with askopenfile(mode="rb", initialdir=FILES_DIR, initialfile=file) as f:
            return pickle.load(f)
    except AttributeError:
        return False
    except Exception:
        traceback.print_exc()
        return False

def exists(file):
    assert file

    file = format_file(file)
    return file in files()
    
def format_file(file):
    assert file

    if not file.endswith(VW_EXTENSION):
        file += VW_EXTENSION
    return file

def files():
    try:
        f = [file for file in os.listdir(FILES_DIR) if file.endswith(".vw")]
        f.sort()
        return f
    except Exception:
        traceback.print_exc()
        return []
