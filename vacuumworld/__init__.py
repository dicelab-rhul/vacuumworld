#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:23:17 2019

@author: Benedict Wilkins
"""

from . import vw
from . import vwv
from . import vwc
from . import vwutils

__all__ = ('vw', 'vwv', 'vwc')


def run(white_mind, green_mind=None, orange_mind=None, **kwargs):
    default_observe = {'grid_size':vwutils.print_observer}
    white_mind, green_mind, orange_mind = vwutils.process_minds(white_mind, green_mind, orange_mind, default_observe)
    
    vwv.run({vwc.colour.white:white_mind, 
             vwc.colour.green:green_mind, 
             vwc.colour.orange:orange_mind}, **kwargs)




