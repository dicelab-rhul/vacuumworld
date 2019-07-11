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

# do some things

import copy

def run(white_agent, green_agent=None, orange_agent=None):
    if green_agent is None:
        green_agent = copy.deepcopy(white_agent)
    if orange_agent is None:
        orange_agent = copy.deepcopy(white_agent)
        
    white_ok = vw.__validate_agent(white_agent, 'white')
    green_ok = vw.__validate_agent(green_agent, 'green')
    orange_ok = vw.__validate_agent(orange_agent, 'orange')
    if white_ok and green_ok and orange_ok:
        vwv.run()


    

