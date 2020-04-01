#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Actions may be attempted by agents at each cycle. An agent can attempt actions by returning them in the ``decide`` method.
An agent can attempt at most one physical action and one speech action per cycle.

Physical Actions
---------

* move - ``move()`` moves the agent one location in the direction of its current ``orientation`` - ``north``, ``east``, ``south`` or ``west``.
* turn - ``turn(direction)`` turns the agent in the given ``direction`` - ``left`` or ``right``.
* clean - ``clean()`` cleans any compatible dirt that is at the agents current ``location``.
* idle - ``idle()`` the agent is idle (no action is attempted).
* drop - ``drop(colour)`` the agent will drop dirt of the given ``colour`` at its current ``location``.

Speech Actions
---------

* speak - ``speak(message, *to)`` sends the given ``message`` to recipient agents specified by their ``name`` in ``*to``. If no recipients are specified the message with be broadcast to all agents.

Example 1
---------
::
    
    def decide(self):
        if self.observation.forward:
            return action.move()
        else:
            return action.idle()

In this example the agent will attempt to move forward until it reaches the edge of the grid (where ``self.observation.foward`` will be ``None``) and will then remain idle.

Example 2
---------
::
    
    def decide(self):
        return action.turn(direction.left), action.speak('hello!')

In this example the agent will spin around anti-clockwise - turning once per cycle, while broadcasting ``'hello'`` to all other agents.
'''

def move():
    '''
        Moves an agent one tile in the direction it is facing.

        Returns: 
            ``('move',)``
    '''
    return ('move',)

def turn(direction):
    '''
        Turns an agent in the given direction ``left`` or``right``. 
        
        Returns: 
            ``('turn', direction)``
    '''
    return ('turn', direction)

def clean():
    '''
        Cleans any compatible dirt at an agents current location. 
        
        Compatibility:
            * Green Agent -> Green Dirt
            * Orange Agent -> Orange Dirt
            * White Agent -> Green & Orange Dirt
            * User -> None
        
        Returns:
            ``('clean',)``
    '''
    return ('clean',)

def idle():
    '''
        The agent is idle (no action is attempted). This is the equivalent of returning ``None``.
        
        Returns:
            ``('idle',)``
    '''
    return ('idle',)

def speak(message, *to):
    '''
        Sends the given ``message`` to recipient agents specified by their ``name`` in ``*to``. If no recipients are specified the message with be broadcast to all agents.
        
        Arguments:
            ``message (str, list, tuple, int, float, bool)``: the message to send.
        
            ``*to (str, variable, optional)``: The recipients of the messages. If empty, the message will be broadcast to all agents.
        
        Returns:
            ``('speak', message, to)``
    '''
    return ('speak', message, to)

def drop(colour):
    '''
        The agent will drop dirt of the given colour at its current location. Only a user agent can perform this action.
        
        Arguments:
            ``colour (vwc.colour)``: The colour of the dirt (``green`` or ``orange``). 
            
        Returns:
            ``('drop', colour)``
    '''
    return ('drop',colour)