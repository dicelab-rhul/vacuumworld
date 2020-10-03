#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:00:27 2019

@author: ben
"""
from . import vwc
from .vwc import action
from .vwutils import ignore



class EasyUser():
    def __init__(self):
        self.observation = None
        self.id = None
        self.move_actions = [action.move(), action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)]
        self.actions = [action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)]
        self.actions.extend(self.move_actions)
        
    def decide(self): 
        if not self.observation.forward: #there is a wall infront
            if not self.observation.left:
                return action.turn(vwc.Direction.right)
            elif not self.observation.right:
                return action.turn(vwc.Direction.left)
            else:
                return vwc.random(self.move_actions[1:])
        #if there is already a dirt at this location, move or turn
        elif self.observation.center.dirt:
            if not self.observation.left:
                return vwc.random(self.move_actions, [0.6, 0.0, 0.4])
            elif not self.observation.right:
                return vwc.random(self.move_actions, [0.6, 0.4, 0.0])
            else:
                return vwc.random(self.move_actions, [0.5, 0.25, 0.25])
        else:
            #otherwise do a random action (including dropping dirt)
            return vwc.random(self.actions, [0.2, 0.2, 0.45, 0.075, 0.075])
            
    def revise(self, observation, messages):
        self.id = observation.center.agent.name
        self.observation = observation

        # A user is not supposed to manage any message.
        ignore(messages)
        
class MediumUser():
    def __init__(self):
        self.observation = None
        self.id = None

    def _decide_if_wall_ahead(self):
        if not self.observation.left: #wall left and forward
            return action.turn(vwc.Direction.right)
        elif not self.observation.right: #wall right and forward
            return action.turn(vwc.Direction.left)
        elif self.observation.left.agent and self.observation.right.agent: #both left and right are full
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        elif self.observation.left.agent: #the left location is full
            return action.turn(vwc.Direction.right)
        elif self.observation.right.agent: #the right location is full
            return action.turn(vwc.Direction.left)
        elif self.observation.center.dirt: #both left and right are free, drop dirt?
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        else:
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)])
        
    def _decide_if_agent_ahead(self):
        if not self.observation.left:
            return action.turn(vwc.Direction.right)
        elif not self.observation.right:
            return action.turn(vwc.Direction.left)
        elif self.observation.left.agent and self.observation.right.agent: #both left and right are full
            return vwc.random([action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)])
        elif self.observation.left.agent: #the left location is full
            return action.turn(vwc.Direction.right)
        elif self.observation.right.agent: #the right location is full
            return action.turn(vwc.Direction.left)
        elif self.observation.center.dirt: #both left and right are free, drop dirt?
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right)])
        else:
            return vwc.random([action.turn(vwc.Direction.left), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)])

    def _decide_if_wall_on_the_left(self):
        if self.observation.center.dirt:
            return vwc.random([action.move(), action.turn(vwc.Direction.right)], [0.9, 0.1])
        else:
            return vwc.random([action.move(), action.turn(vwc.Direction.right), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    def _decide_if_wall_on_the_right(self):
        if self.observation.center.dirt:
            return vwc.random([action.move(), action.turn(vwc.Direction.left)], [0.9, 0.1])
        else:
            return vwc.random([action.move(), action.turn(vwc.Direction.left), action.drop(vwc.Colour.green), action.drop(vwc.Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    def decide(self): 
        # Wall ahead
        if not self.observation.forward:
            return self._decide_if_wall_ahead() 
        # Agent ahead
        elif self.observation.forward.agent:
            return self._decide_if_agent_ahead()
        # If there is an agent in some direction, turn to face away from it aslong as there isnt a wall
        elif self.observation.left and self.observation.left.agent and self.observation.right and self.observation.right.agent:
            return MediumUser.move_or_drop()
        elif self.observation.left and self.observation.left.agent and self.observation.right:
            return vwc.random([action.turn(vwc.Direction.right), action.move()])
        elif self.observation.right and self.observation.right.agent and self.observation.left:
            return vwc.random([action.turn(vwc.Direction.left), action.move()])
        elif not self.observation.left:
            self._decide_if_wall_on_the_left()
        elif not self.observation.right:
            self._decide_if_wall_on_the_right()
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
