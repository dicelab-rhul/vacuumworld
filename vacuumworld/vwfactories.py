# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:34:00 2019

@author: Nausheen Saba


"""
from pystarworlds.Factories import PerceptionFactory, Precondition, Executor
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction

#from .vwperception import Observation
from . import vwaction
from . import vwc

ORIENTATION = {'north':vwc.coord(0,-1), 'south':vwc.coord(0,1), 'west':vwc.coord(-1,0), 'east':vwc.coord(1,0)}

class ObservationFactory(PerceptionFactory):
    
    def __init__(self):
        super(ObservationFactory, self).__init__(vwc.observation)
        
    def __call__(self, ambient, agent):
        c = agent.coordinate
        f = ORIENTATION[agent.orientation]
        l = ORIENTATION[vwc.left(agent.orientation)]
        r = ORIENTATION[vwc.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = vwc.observation(ambient.grid.state[c], 
                        ambient.grid.state[c + l],
                        ambient.grid.state[c + r], 
                        ambient.grid.state[c + f], 
                        ambient.grid.state[c + f + l],
                        ambient.grid.state[c + f + r])            
        return obs
    

class MovePrecondition(Precondition):
        
    def __init__(self):
         super(MovePrecondition, self).__init__(vwaction.MoveAction)
    
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
         #a bit inefficient, may we can rethink preconditons and executors, they could be the same class.
        new_coordinate = agent.coordinate + ORIENTATION[agent.orientation]
        new_location = env.ambient.grid.state[new_coordinate]
        #print("MOVE PRECONDITION:", agent.ID, new_location != None and new_location.agent == None)
        return new_location != None and new_location.agent == None
    
class CleanPrecondition(Precondition):
        
    def __init__(self):
         super(CleanPrecondition, self).__init__(vwaction.CleanAction)
    
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        #print("CLEAN PRECONDITION:", agent.ID, env.ambient.grid.state[agent.coordinate].dirt != None)
        return env.ambient.grid.state[agent.coordinate].dirt != None
    
class DropPrecondition(Precondition):
        
    def __init__(self):
         super(DropPrecondition, self).__init__(vwaction.DropAction)
    
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        #print("DROP PRECONDITION:", agent.ID, env.ambient.grid.state[agent.coordinate].dirt == None)
        return env.ambient.grid.state[agent.coordinate].dirt == None
    
class CommunicationFactory(PerceptionFactory):
    
    def __init__(self):
        super(CommunicationFactory, self).__init__(vwc.message)

    def __call__(self, _, event):
        return vwc.message(event.sender, event.content)

class CommunicationExecutor(Executor):

    def __init__(self):
        super(CommunicationExecutor, self).__init__(vwaction.CommunicativeAction)
        self.percept_factory = CommunicationFactory() 
        
    def __call__(self, env, action):
        notify = action.to
        if len(notify) == 0: #send to everyone! do we want this?
            notify = set(env.ambient.agents.keys()) - set([action.__actor__])
        
        #print(action.__actor__, "->", notify)
        
        for to in notify:
            env.physics.notify_agent(env.ambient.agents[to], self.percept_factory(None, action))
        
class MoveExecutor(Executor):
    
    def __init__(self):
        super(MoveExecutor, self).__init__(vwaction.MoveAction)
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        new_coordinate = agent.coordinate + ORIENTATION[agent.orientation]
        env.ambient.grid.move_agent(agent.coordinate, new_coordinate)
        agent.coordinate = new_coordinate
        
class TurnExecutor(Executor):
    
    def __init__(self):
        super(TurnExecutor, self).__init__(vwaction.TurnAction)
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        new_orientation = action.direction(agent.orientation)
        env.ambient.grid.turn_agent(agent.coordinate, new_orientation)
        agent.orientation = new_orientation

class CleanExecutor(Executor):
    
    def __init__(self):
        super(CleanExecutor, self).__init__(vwaction.CleanAction)
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        env.ambient.grid.remove_dirt(agent.coordinate)

class DropExecutor(Executor):
    
    def __init__(self):
        super(DropExecutor, self).__init__(vwaction.DropAction)
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        env.ambient.grid.place_dirt(agent.coordinate, env.ambient.dirt(action.colour))
             
        