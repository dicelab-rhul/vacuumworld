#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:00:27 2019

@author: ben
"""
from . import vwc
from .vwc import action
from .vwutils import ignore


class User():
    def __init__(self):
        self.observation = None
        self.id = None

    def decide(self):
        raise NotImplementedError("Abstract class.")

    def revise(self, observation, messages):
        raise NotImplementedError("Abstract class.")

    def is_wall_ahead(self):
        return not self.observation.forward

    def is_wall_on_the_left(self):
        return not self.observation.left

    def is_wall_on_the_right(self):
        return not self.observation.right

    def is_on_dirt(self):
        return self.observation.center.dirt

    def is_agent_ahead(self):
        return self.observation.forward and self.observation.forward.agent

    def is_agent_on_the_left(self):
        return self.observation.left and self.observation.left.agent

    def is_agent_of_the_right(self):
        return self.observation.right and self.observation.right.agent


class EasyUser(User):
    def __init__(self):
        super().__init__()
        self.move_actions = [action.move(), action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)]
        self.actions = [action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)]
        self.actions.extend(self.move_actions)
        
    def _decide_if_wall_ahead(self):
        if self.is_wall_on_the_left():
            return action.turn(vwc.Direction.right)
        elif self.is_wall_on_the_right():
            return action.turn(vwc.Direction.left)
        else:
            return vwc.random(self.move_actions[1:])

    def _decide_if_on_dirt(self):
        if self.is_wall_on_the_left():
            return vwc.random(self.move_actions, [0.6, 0.0, 0.4])
        elif self.is_wall_on_the_right():
            return vwc.random(self.move_actions, [0.6, 0.4, 0.0])
        else:
            return vwc.random(self.move_actions, [0.5, 0.25, 0.25])

    def decide(self): 
        if self.is_wall_ahead():
            return self._decide_if_wall_ahead()
        elif self.is_on_dirt():
            #if there is already a dirt at this location, move or turn
            return self._decide_if_on_dirt()
        else:
            #otherwise do a random action (including dropping dirt)
            return vwc.random(self.actions, [0.2, 0.2, 0.45, 0.075, 0.075])
            
    def revise(self, observation, messages):
        self.id = observation.center.agent.name
        self.observation = observation

        # A user is not supposed to manage any message.
        ignore(messages)
        
class MediumUser(User):
    # Always wall ahead
    def _decide_if_wall_ahead(self):
        if self.is_wall_on_the_left(): # wall on the left
            return action.turn(vwc.Direction.right)
        elif self.is_wall_on_the_right(): # wall on the right
            return action.turn(vwc.Direction.left)
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right(): # both left and right are full
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        elif self.is_agent_on_the_left(): # agent on the left
            return action.turn(vwc.Direction.right)
        elif self.is_agent_of_the_right(): # agent on the right
            return action.turn(vwc.Direction.left)
        elif self.is_on_dirt(): # both left and right are free, drop dirt?
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        else: # wall ahead, left and right free, no dirt on center.
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)])
        
    # Always agent ahead
    def _decide_if_agent_ahead(self):
        if self.is_wall_on_the_left():
            return action.turn(vwc.Direction.right)
        elif not self.is_wall_on_the_right():
            return action.turn(vwc.Direction.left)
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right(): # both left and right are full
            return vwc.random([action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)]) #TODO: is this logic correct? Compare with the method above.
        elif self.is_agent_on_the_left(): # agent on the left
            return action.turn(vwc.Direction.right)
        elif self.is_agent_of_the_right(): # agent on the right
            return action.turn(vwc.Direction.left)
        elif self.is_on_dirt(): # both left and right are free, drop dirt?
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        else:
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)])

    # Always wall on the left
    def _decide_if_wall_on_the_left(self):
        if self.is_on_dirt():
            return vwc.random([action.move(), action.turn(vwc.Direction.right)], [0.9, 0.1])
        else:
            return vwc.random([action.move(), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    # Always wall on the right
    def _decide_if_wall_on_the_right(self):
        if self.is_on_dirt():
            return vwc.random([action.move(), action.turn(vwc.Direction.left)], [0.9, 0.1])
        else:
            return vwc.random([action.move(), action.turn(vwc.Direction.left), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    def decide(self): 
        # Wall ahead
        if self.is_wall_ahead():
            return self._decide_if_wall_ahead()
        # Agent ahead
        elif self.is_agent_ahead():
            return self._decide_if_agent_ahead()
        # Right and left occupied
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right():
            return MediumUser.move_or_drop()
        # Agent on the left and no wall on the right
        elif self.is_agent_on_the_left() and not self.is_wall_on_the_right():
            return vwc.random([action.turn(vwc.Direction.right), action.move()])
        # Agent on the right and no wall on the left
        elif self.is_agent_of_the_right() and not self.is_wall_on_the_left():
            return vwc.random([action.turn(vwc.Direction.left), action.move()])
        # Wall on the left
        elif self.is_wall_on_the_left():
            return self._decide_if_wall_on_the_left()
        # Wall on the right
        elif self.is_wall_on_the_right():
            return self._decide_if_wall_on_the_right()
        # Any other possibility
        else:
            return MediumUser.random_all()         
    
    @staticmethod
    def move_or_drop():
        return vwc.random([action.move(), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)], [0.8, 0.1, 0.1])   
     
    @staticmethod
    def random_all():
        return vwc.random([action.move(), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange),
                           action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)], [0.6, 0.15, 0.15, 0.05, 0.05]) 
            
    def revise(self, observation, messages):
        self.id = observation.center.agent.name
        self.observation = observation

        # A user is not supposed to manage any message.
        ignore(messages)

#the users that can be used in vacuumworld
USERS = [EasyUser, MediumUser]
