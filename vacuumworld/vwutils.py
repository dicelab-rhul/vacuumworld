#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 10:29:55 2019

@author: ben
"""
from pystarworlds.Agent import Mind

import inspect

def callerID():
    caller = inspect.currentframe().f_back
    while not isinstance(caller.f_locals.get('self', None), Mind):
        caller = caller.f_back
    return caller.f_locals['self'].body.ID

def warn_agent(message, *args):
    print(message.format(callerID(), *args))