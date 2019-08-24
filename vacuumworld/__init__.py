#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:23:17 2019

@author: ben
"""

from . import vw
from . import vwv
from . import vwc

__all__ = ('vw', 'vwv', 'vwc')



__MARKING = False
__CURRENT = None

def run(white_mind, green_mind=None, orange_mind=None):

    
    if green_mind is None:
        green_mind = white_mind
    if orange_mind is None:
        orange_mind = white_mind
    
    if __MARKING:
        __MARKING_HASH = r'c0bd538fd8bdaac7a98802fd9f0ddda29aa6bea3705e88b9dc32ab5d4821fa58'
        __MARKING_PASSWORD_FILE = 'password.txt'
        import hashlib
        with open(__MARKING_PASSWORD_FILE, 'rb') as f:
             password = f.readline()
             m = hashlib.sha256(password)
             if m.hexdigest() == __MARKING_HASH:
                 #import vacuumworldmarking #import the marking module
                 global __CURRENT
                 if __CURRENT is not None:
                      raise ValueError("Student called run more than once... oh dear")
                 __CURRENT = (white_mind, green_mind, orange_mind)  
             else:
                 raise ValueError('Incorrect marking password')
    else:
        white_ok = vw.__validate_mind(white_mind, 'white')    
        green_ok = vw.__validate_mind(green_mind, 'green')
        orange_ok = vw.__validate_mind(orange_mind, 'orange')
        if white_ok and green_ok and orange_ok:
            vwv.run({vwc.colour.white:white_mind, 
                     vwc.colour.green:green_mind, 
                     vwc.colour.orange:orange_mind})


def grid_size(agent_id, size):
    assert(isinstance(agent_id, str))
    #for marking purposes

