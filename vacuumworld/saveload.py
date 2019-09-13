#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
"""

import os
import pickle
import traceback

FILE_PATH = "files/"

def init():
    if not os.path.isdir("./" + FILE_PATH):
        os.mkdir("./" + FILE_PATH)
    
def save(grid, file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    try: 
        with open(FILE_PATH + file, 'wb') as f:
             pickle.dump(grid, f)
    except:
        traceback.print_exc()
    
def load(file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    try:
        with open(FILE_PATH + file, 'rb') as f:
            return pickle.load(f)
    except:
        traceback.print_exc()


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

