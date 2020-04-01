#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VacuumWorld Constants
---------
``vwc`` defines a number of convenience classes and functions 
that should be used when implementing an agent mind, including actions and observations. 

Full documentation and detailed explaination is provided in the VacuumWorld Guide 
avaliable on the course moodle page. 

"""

__author__ = "Benedict Wilkins"
__license__ = "GPL"
__version__ = "4.1.7"
__maintainer__ = "Benedict Wilkins"
__email__ = "zavc926@live.rhul.ac.uk"

import random as rand
import typing
from enum import Enum
from . import action

__all__ = ('action', 'observation', 'location', 'direction', 'agent', 'dirt', 'coord', 'size', 'random')

class orientation(Enum):
    '''
        Representation of an agents orientation. An agent can be orientated in 
        one of the cardinal directions (north, east, south, west). This class is useful
        for checking in which of theese directions the agent is facing.
        
        Example
        --------
        ::
            
            from vwc import action, direction, orientation
            
            def revise(self, observation, messages):
                self.orientation = observation.center.agent.orientation
            
            def decide(self):
                if self.orientation == orientation.north:
                    return action.turn(direction.right)
                
        
        If the agent is facing northward it will turn to the right.
        
        Attributes:
            * ``north``
            * ``east``
            * ``south``
            * ``west``
    '''
    north = 'north'
    east = 'east'
    south = 'south'
    west = 'west'

    def __eq__(self, other):
        return super().__eq__(other) or self.value == other

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)
    
class colour(Enum):
    '''
        Representation of colour. Both dirt and agents have a colour (green, orange, white, user).
        
        * A cleaning agent may be green, orange or white;
        * A user agent always has the user colour;
        * A dirt may be green or orange.
        The colour an agent determins its cleaning capability, see ``action.clean``.
        
        Attributes:
            * ``green``
            * ``orange``
            * ``white``
            * ``user``
    '''
    
    green = 'green'
    orange = 'orange'
    white = 'white'
    user = 'user'
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)

#todo remove these
_colour_dirt = set(['orange','green'])
_colour_agent = set(['orange','green','white'])
_colour_user = set(['user'])

class coord(typing.NamedTuple):
    '''
        A coordinate ``(x,y)``. Standard arethmetic operations ``(+ - * / //)`` can be performed on this object.
        
        Note that division (/ //) is always integer division.
        
        Attributes:
            * ``x (int)``: x component.
            * ``y (int)``: y component.
    '''
    x : int
    y : int

    def __add__(self, other):
        if isinstance(other, int):
            return coord(self[0] + other, self[1] + other)
        return coord(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        if isinstance(other, int):
            return coord(self[0] - other, self[1] - other)
        return coord(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other):
        if isinstance(other, int):
            return coord(self[0] * other, self[1] * other)
        return coord(self[0] * other[0], self[1] * other[1])
    
    def __truediv__(self, other):
        if isinstance(other, int):
            return coord(self[0] // other, self[1] // other)
        return coord(self[0] // other[0], self[1] // other[1])

    def __floordiv__(self, other):
        return self / other

class agent(typing.NamedTuple):
    '''
        A datastructure representing an agent in an observation.
        
        Attributes:
            * ``name (str)``: the name of the agent.
            * ``colour (vwc.colour)``:  the colour of the agent.
            * ``orientation (vwc.orientation)``: the orientation of the agent.
    '''
    name : str
    colour : colour
    orientation : orientation

class dirt(typing.NamedTuple):
    '''
        A datastructure representing a dirt in an observation.
        Attributes:
            * ``name  (str)``: the name of the dirt.
            * ``colour (vwc.colour)``: the colour of the dirt.
    '''
    name : str 
    colour : colour
    
class location(typing.NamedTuple):
    '''
        A datastructure representing an observed location in the vacuumworld grid. 
        
        Attributes:
            * ``coordinate (vwc.coord)``: The coordinate of the location.
            * ``agent (vwc.agent)``: The agent at this location, ``None`` if there is no agent. 
            * ``dirt (vwc.dirt) ``:The dirt at this location, ``None`` if there is no dirt. 
    '''
    coordinate : coord
    agent : agent
    dirt : dirt

#perception = namedtuple('perception', 'observation messages')

class message(typing.NamedTuple):
    '''
        A datastructure representing a message (perception) of the agent. 
        The content of a message is limited to 100 characters and will be greedily trimmed to fit. 
        To prevent loss of data in the content you should always check the length before sending, or 
        at least have some consideration for the message length in your implementing of an agent mind. 
        ``vwc.size(message)`` can be used to properly check the length of a message.
        Attributes:
            * ``sender (str)``: The name of the sender of the message.
            * ``content (str, list, tuple, int, float, bool)``: The content of the message.
    '''
    sender : str
    content : typing.Union[str, list, tuple, float, bool]

class observation(typing.NamedTuple):
    '''
        A datastructure representing an observation (perception) of the agent. 
        An observation consists of six locations, the center location always 
        contains the observing agent. Each of the other 5 locations are relative 
        to the center location.
        
        Example 1
        -----------
        ::
            
            def revise(self, observation, messages):
                self.observation = observation
                self.colour = observation.center.agent.colour
                self.position = observation.center.agent.coordinate
        
        An agent should update its beliefs with new information that it has 
        perceived for later use in decision making.
        
        Example 2
        ----------
        ::
            
            def decide(self):
                if self.observation.forward.agent:
                    return action.turn(direction.left)
                elif self.observation.forward:
                    return action.move()
                else:
                    return action.idle()
                    
        This agent will turn if there is an agent in-front of it, move until it 
        reachs the edge of the grid and then remains idle.
    '''
    center : location
    left : location
    right : location
    forward : location
    forwardleft : location
    forwardright : location

    def __iter__(self):
        return (self[i] for i in range(len(self)) if self[i] is not None)

class direction:
    '''
        An indicator used in the turn action. May also be used to turn orientations.
        
        Attributes:
            * `left (callable)`: Turns an orientation left,  indicates a left turn in the turn action.  
            * `right (callable)`: Turns an orientation right,  indicates a right turn in the turn action.  
        
        Example 1
        ---------
        ::
            
            def decide(self):
                return action.turn(direction.left)
                
        Example 2
        ---------
        ::
            
            def revise(self, observation, messages):
                self.orientation = observation.center.agent.orientation
                self.left_orientation = direction.left(self.orientation)
                self.right_orientation = direction.right(self.orientation)
    '''

    def left(_orientation):
        '''
            Turns an orientation left. Indicates a left turn in the turn action.                        
        '''
        od = (orientation.north, orientation.east, orientation.south, orientation.west)
        return od[(od.index(_orientation) - 1) % 4]

    def right(_orientation):
        '''
            Turns an orientation left. Indicates a left turn in the turn action.                        
        '''
        od = (orientation.north, orientation.east, orientation.south, orientation.west)
        return od[(od.index(_orientation) + 1) % 4]


def size(message):
    '''
        Computes the size of a message.
        
        Argument:
            * ``message (str, list, tuple, int, float, bool)``: to check the size of.
        
        Returns:
            ``(int)``: The size of the message.
            
        Example
        --------
        ::
            
            >>> size('hello')
            5
            >>> size(('size', 9))
            8
            >>> size(['hello', ('size', 9)])
            16
            
    '''
    _size = 0
    if type(message) in (list, tuple): 
        _size += len(message) + 1
        for e in message:
            _size += size(e)
    elif message is not None:
        _size += len(str(message))
    return _size

def random(actions, p=None):
    '''
        Selects a random action from ``actions`` with given probabilities ``p``. 
        If ``p`` is ``None`` then the action will be selected uniformly.
        Otherwise, both arguments should have the same length.
        
        Arguments:
            * ``actions (list)``: a list of actions to choose from.
            * ``p (list)``:  a list of probabilities, one per action in ``actions`` that sum to 1, or ``None``.
            
        Returns:
           ``(any)``: the selected action.
           
        Example
        ----------
        ::
            
            def decide(self):
                return random([action.move(), action.turn(direction.left)], [0.8, 0.2])
        
        The agent will move with 0.8 probability and turn left with 0.2 probability.
    '''
    if p is None:
        return rand.choice(actions)
    else:
        assert len(actions) == len(p)
        return rand.choices(actions, weights=p, k=1)[0]