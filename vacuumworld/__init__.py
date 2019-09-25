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

__MARKING = False
__CURRENT = None
__OBSERVE = {'grid_size':None}


def run(white_mind, green_mind=None, orange_mind=None, **kwargs):

    def __validate_mind(mind, colour, observe):
        for obs in observe:
            if not obs in set(dir(mind)):
                raise vw.VacuumWorldInternalError("{0} agent: must define the attribute: {1}, (see coursework question 1)".format(colour, obs)) 
        def sneaky_setattr(self, name, value):
            if name in observe: 
                if observe[name] == None:
                    print("Agent {0} updated {1}: {2}".format(vwutils.callerID(), name, value))
                else:
                    observe[name](mind, colour, name, value)
            super(type(mind), self).__setattr__(name, value)
            
        type(mind).__setattr__ = sneaky_setattr
        
        return vw.__validate_mind(mind, colour)
        
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
        white_ok = __validate_mind(white_mind, 'white', __OBSERVE)    
        green_ok = __validate_mind(green_mind, 'green', __OBSERVE)
        orange_ok = __validate_mind(orange_mind, 'orange', __OBSERVE)
        
        #must contain grid_size... for the coursework, really we should place this somewhere else as it is not general!
        
        if white_ok and green_ok and orange_ok:
            vwv.run({vwc.colour.white:white_mind, 
                     vwc.colour.green:green_mind, 
                     vwc.colour.orange:orange_mind}, **kwargs)




