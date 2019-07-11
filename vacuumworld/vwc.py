#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 21:53:28 2019

@author: ben
"""

from collections import namedtuple

location = namedtuple('location', 'coordinate agent dirt')
agent = namedtuple('agent', 'name colour direction')
dirt = namedtuple('dirt', 'name colour')
coord = namedtuple('coordinate', 'x y')

perception = namedtuple('perception', 'observation messages')

message = namedtuple('message', 'sender content')
observation = namedtuple('observation', 'center left right forward forwardleft forwardright')

direction = namedtuple('direction', 'north east south west')('north', 'east', 'south', 'west')
colour = namedtuple('colour', 'white orange green user')('white', 'orange', 'green', 'user')


perception_types = namedtuple('types', 'message observation')('message', 'observation')


def is_colour(c):
    return c in set(colour._fields)

def is_direction(d):
    return d in set(direction._fields)


class ActionFactory:
    
    def __init__(self, name):
        self.name = name
    
    def __call__(self):
        return (self.name,)

class SpeakActionFactory(ActionFactory):
    
    def __init__(self, name):
        super(SpeakActionFactory, self).__init__(name)
        
    def __call__(self, _message, *_to):
        assert(isinstance(_message, str))
        for t in _to:
            assert(isinstance(t, str))
        return (self.name, _message, *_to)

action = namedtuple('actions', 'move turn_left, turn_right clean idle speak')(\
        ActionFactory('move'), ActionFactory('turn_left'), ActionFactory('turn_right'), 
        ActionFactory('clean'), ActionFactory('idle'), SpeakActionFactory('speak'))







