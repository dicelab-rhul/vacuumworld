#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 21:53:28 2019

@author: ben
"""
import random as rand
from collections import namedtuple

location = namedtuple('location', 'coordinate agent dirt')
agent = namedtuple('agent', 'name colour orientation')
dirt = namedtuple('dirt', 'name colour')
_coord = namedtuple('coordinate', 'x y')

class coord(_coord):
    
    def __add__(self, other):
        return coord(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        return coord(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other):
        return coord(self[0] * other[0], self[1] * other[1])
    
    def __div__(self, other):
        return coord(int(self[0] / other[0]), int(self[1] / other[1]))
    


perception = namedtuple('perception', 'observation messages')

message = namedtuple('message', 'sender content')

_observation = namedtuple('observation', 'center left right forward forwardleft forwardright')

class observation(_observation):
    def __iter__(self):
        return (x for x in super(observation, self).__iter__() if x is not None)

orientation = namedtuple('orientation', 'north east south west')('north', 'east', 'south', 'west')

orientation_map = {orientation.north:coord(0,-1), 
                   orientation.south:coord(0,1), 
                   orientation.west:coord(-1,0), 
                   orientation.east:coord(1,0)}

def left(_orientation):
    return orientation[(orientation.index(_orientation) - 1) % 4]

def right(_orientation):
    return orientation[(orientation.index(_orientation) + 1) % 4]

direction = namedtuple('direction', 'left right')(left, right)

colour = namedtuple('colour', 'white orange green user')('white', 'orange', 'green', 'user')

_colour_dirt = set(['orange','green'])
_colour_agent = set(['orange','green','white'])
_colour_user = set(['user'])

action_names = namedtuple('action_names', 'move turn clean drop idle speak')('move','turn','drop','clean','idle','speak')

action = namedtuple('actions', 'move turn clean idle speak')(
                    lambda : ('move',), 
                    lambda _direction : ('turn', _direction), 
                    lambda : ('clean',), 
                    lambda : None, 
                    lambda message, *to : ('speak', message, *to))

def random(actions, p=None):
    if p is None:
        return rand.choice(actions)
    else:
        assert len(actions) == len(p)
        return rand.choices(actions, weights=p, k=1)[0]



