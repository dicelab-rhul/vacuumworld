#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
"""

import os
import pickle

def save(grid, file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    with open(file, 'wb') as f:
         pickle.dump(grid, f)
    
def load(file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    with open(file, 'rb') as f:
        return pickle.load(f)

def exists(file):
    file = format_file(file)
    return file in files()
    
def format_file(file):
    if not file.endswith('.vw'):
        file = file + ".vw"
    return file

def files():
    return [file for file in os.listdir('.') if file.endswith(".vw")]
    

