# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:34:00 2019

@author: Nausheen Saba


"""
from pystarworlds.Factories import PerceptionFactory, Rule,Executor
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction

#from .vwperception import Observation
from .vw import Grid
from . import vwaction
from . import vwc

class ObservationFactory(PerceptionFactory):
    
    def __init__(self):
        super(ObservationFactory, self).__init__(vwc.observation)
        
    def __call__(self, ambient, agent):
        c = agent.coordinate
        f = Grid.DIRECTIONS[agent.orientation]
        l = Grid.DIRECTIONS[vwc.left(agent.orientation)]
        r = Grid.DIRECTIONS[vwc.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = vwc.observation(ambient.grid.state[c], 
                        ambient.grid.state[vwc.add(c, l)],
                        ambient.grid.state[vwc.add(c, r)], 
                        ambient.grid.state[vwc.add(c, f)], 
                        ambient.grid.state[vwc.add(vwc.add(c,f),l)],
                        ambient.grid.state[vwc.add(vwc.add(c,f),r)])
        print("observation")
        for x in obs:
            print("->", x)
            
        return obs
    
    
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
        agent = env.ambient[action.owner]
        env.physics.notify_agent(agent, self.percept_factory())
        
'''
class SpeakActionExecuteFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.SpeakAction)
        
    
    def __call__(self, env, action):
        action.execute(env)          
'''
        