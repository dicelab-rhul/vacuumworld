#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
"""

import os
import pickle
import traceback

from tkinter.filedialog import asksaveasfile, askopenfile

FILE_PATH = "files/"

def init():
    if not os.path.isdir("./" + FILE_PATH):
        os.mkdir("./" + FILE_PATH)
    

def save_dialog(grid, file=""):
    try:
        if file != "" and not  file.endswith(".vw"):
            file = file + ".vw"

        with asksaveasfile(mode="wb", initialdir=os.path.join(os.getcwd(), "files"), initialfile=file, defaultextension=".vw") as f:
            pickle.dump(grid, f)
            return True
    except AttributeError:
        return False
    except:
        traceback.print_exc()
        return False

'''
def save(grid, file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    try: 
        with open(FILE_PATH + file, 'wb') as f:
             pickle.dump(grid, f)
    except:
        traceback.print_exc()
'''

def load_dialog(file=""):
    try:
        if file != "" and not  file.endswith(".vw"):
            file = file + ".vw"

        with askopenfile(mode="rb", initialdir=os.path.join(os.getcwd(), "files"), initialfile=file) as f:
            return pickle.load(f)
    except AttributeError:
        return False
    except:
        traceback.print_exc()
        return False

'''
def load(file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    try:
        with open(FILE_PATH + file, 'rb') as f:
            return pickle.load(f)
    except:
        traceback.print_exc()
'''


def exists(file):
    file = format_file(file)
    return file in files()
    
def format_file(file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    return file

def files():
    try:
        f = [file for file in os.listdir('./' + FILE_PATH) if file.endswith(".vw")]
        f.sort()
        return f
    except:
        traceback.print_exc()
        return []

