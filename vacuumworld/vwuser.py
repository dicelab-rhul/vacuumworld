#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:00:27 2019

@author: ben
"""
from . import vwc
from .vwc import action



class EasyUser:
    
    def __init__(self):
        self.observation = None
        self.id = None
        self.move_actions = [action.move(), action.turn(vwc.direction.left), action.turn(vwc.direction.right)]
        self.actions = [action.drop(vwc.colour.green), action.drop(vwc.colour.orange)]
        self.actions.extend(self.move_actions)
        
    def decide(self): 

        if not self.observation.forward: #there is a wall infront
            if not self.observation.left:
                return action.turn(vwc.direction.right)
            if not self.observation.right:
                return action.turn(vwc.direction.left)
            return vwc.random(self.move_actions[1:])
        
        #if there is already a dirt at this location, move or turn
        if self.observation.center.dirt:
            if not self.observation.left:
                return vwc.random(self.move_actions, [0.6, 0.0, 0.4])
            if not self.observation.right:
                return vwc.random(self.move_actions, [0.6, 0.4, 0.0])
            return vwc.random(self.move_actions, [0.5, 0.25, 0.25])
    
        #otherwise do a random action (including dropping dirt)
        return vwc.random(self.actions, [0.2, 0.2, 0.45, 0.075, 0.075])
            
    def revise(self, observation, messages):
        self.id = observation.center.agent.name
        self.observation = observation
        
class MediumUser:

    def __init__(self):
        self.observation = None
        self.id = None
        
    def decide(self): 
        #there is a wall forward of the agent
        if not self.observation.forward:
            if not self.observation.left: #wall left and forward
                return action.turn(vwc.direction.right)
            if not self.observation.right: #wall right and forward
                return action.turn(vwc.direction.left)
            if self.observation.left.agent and self.observation.right.agent: #both left and right are full
                return vwc.random([action.turn(vwc.direction.left), action.turn(vwc.direction.right)])
            if self.observation.left.agent: #the left location is full
                return action.turn(vwc.direction.right)
            if self.observation.right.agent: #the right location is full
                return action.turn(vwc.direction.left)
            if self.observation.center.dirt: #both left and right are free, drop dirt?
                return vwc.random([action.turn(vwc.direction.left), action.turn(vwc.direction.right)])
            return vwc.random([action.turn(vwc.direction.left), action.turn(vwc.direction.right),
                               action.drop(vwc.colour.green), action.drop(vwc.colour.orange)])
            
        if self.observation.forward.agent:
            if not self.observation.left:
                return action.turn(vwc.direction.right)
            if not self.observation.right:
                return action.turn(vwc.direction.left)
            if self.observation.left.agent and self.observation.right.agent: #both left and right are full
                return vwc.random([action.drop(vwc.colour.green), action.drop(vwc.colour.orange)])
            if self.observation.left.agent: #the left location is full
                return action.turn(vwc.direction.right)
            if self.observation.right.agent: #the right location is full
                return action.turn(vwc.direction.left)
            if self.observation.center.dirt: #both left and right are free, drop dirt?
                return vwc.random([action.turn(vwc.direction.left), action.turn(vwc.direction.right)])
            return vwc.random([action.turn(vwc.direction.left), action.turn(vwc.direction.right),
                               action.drop(vwc.colour.green), action.drop(vwc.colour.orange)])
        
        #if there is an agent in some direction, turn to face away from it aslong as there isnt a wall
        if self.observation.left and self.observation.left.agent and self.observation.right and self.observation.right.agent:
            return self.move_or_drop()
        if self.observation.left and self.observation.left.agent and self.observation.right:
            return vwc.random([action.turn(vwc.direction.right), action.move()])
        if self.observation.right and self.observation.right.agent and self.observation.left:
            return vwc.random([action.turn(vwc.direction.left), action.move()])
        
        if not self.observation.left:
            if self.observation.center.dirt:
                return vwc.random([action.move(), action.turn(vwc.direction.right)], [0.9, 0.1])
            return vwc.random([action.move(), action.turn(vwc.direction.right),
                               action.drop(vwc.colour.green), action.drop(vwc.colour.orange)], [0.6, 0.25, 0.075, 0.075])
        
        if not self.observation.right:
            if self.observation.center.dirt:
                return vwc.random([action.move(), action.turn(vwc.direction.left)], [0.9, 0.1])
            return vwc.random([action.move(), action.turn(vwc.direction.left),
                               action.drop(vwc.colour.green), action.drop(vwc.colour.orange)], [0.6, 0.25, 0.075, 0.075])
        return self.random_all()         
    
    def move_or_drop(self):
        return vwc.random([action.move(), action.drop(vwc.colour.green), action.drop(vwc.colour.orange)], [0.8, 0.1, 0.1])   
     
    def random_all(self):
        return vwc.random([action.move(), action.drop(vwc.colour.green), action.drop(vwc.colour.orange),
                           action.turn(vwc.direction.left), action.turn(vwc.direction.right)], [0.6, 0.15, 0.15, 0.05, 0.05]) 
            
    def revise(self, observation, messages):
        self.id = observation.center.agent.name
        self.observation = observation

#the users that can be used in vacuumworld
USERS = [EasyUser, MediumUser]
