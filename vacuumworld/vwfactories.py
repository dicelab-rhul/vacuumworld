# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:34:00 2019

@author: Nausheen Saba


"""
from pystarworlds.Factories import PerceptionFactory,Rule,Executor
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction

#from .vwperception import Observation
from .vw import Grid
from . import vwaction
from . import vwc

class VWObservationFactory(PerceptionFactory):
    
    def __init__(self):
        super().__init__(vwc.observation)
        
    def __call__(self, ambient, sensor):
        sensor.owner
        agent = ambient.agents[sensor.owner]
        c = agent.coordinate
        f = Grid.DIRECTIONS[agent.orientation]
        l = Grid.DIRECTIONS[vwc.left(agent.orientation)]
        r = Grid.DIRECTIONS[vwc.right(agent.orientation)]
        obs = vwc.observation(ambient.grid.state[c], 
                        ambient.grid.state[vwc.add(c, f)], 
                        ambient.grid.state[vwc.add(c, l)],
                        ambient.grid.state[vwc.add(c, r)], 
                        ambient.grid.state[vwc.add(vwc.add(c,f),l)],
                        ambient.grid.state[vwc.add(vwc.add(c,f),r)])
        return obs
    
class ForwardActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.ForwardMoveMentAction)
    
    def __call__(self, env, action):
       flag=True
       if(env.getAmbient().getPlacementMap().isOutsideGrid(action.getnewCoordinate())):
         flag=False
       elif(env.getAmbient().getPlacementMap().isOccupiedByActor(action.getnewCoordinate())): 
         flag=False
        
       return flag             
       
class TurnLeftActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.MoveLeftAction)
        
    
    def __call__(self, env, action):
       flag=True
      # if(ambient.getPlacementMap().notValidOrientation(action.getOrient())):
       #    flag=False  
       return flag             
       
class TurnRightActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.MoveRightAction)
        
    
    def __call__(self, env, action):
       flag=True
       if(self.notValidOrientation(action.getOrient())):
           flag=False  
       return flag             
       
    def notValidOrientation(self, actorOrient):
       if actorOrient=="west" or actorOrient=="east" or actorOrient=="south" or actorOrient=="north":
         return False
       else:
         return True
      
    
    
class CleanActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.CleanDirtAction)
        
    
    def __call__(self, env, action):
       flag=True
       if(env.getAmbient().getPlacementMap().isUser(action.getActor())): 
          flag=False  
       if(env.getAmbient().getPlacementMap().agentSittingOnDirt(action.getCoordinate())): 
          loc=env.getAmbient().getPlacementMap().getlocation(action.getCoordinate())
          if not(self.isCompatible(loc.agent.colour,loc.dirt.colour)):
            flag=False
       return flag

             
    def isCompatible(self, actorColor,dirtColor):
       if(actorColor=="white" and (dirtColor=="green" or dirtColor=="orange")):
         return True
       elif(actorColor=="green" and dirtColor=="green"):
         return True
       elif(actorColor=="orange" and dirtColor=="orange"):
         return True
       else:
         return False   
class DropActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.DropDirtAction)
        
    
    def __call__(self, env, action):
       flag=True
       if( not(env.getAmbient().getPlacementMap().isUser(action.getActor()))): 
          flag=False  
       if(env.getAmbient().getPlacementMap().agentSittingOnDirt(action.getCoordinate())): 
          flag=False
       return flag             
class SpeakActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.SpeakAction)
        
    
    def __call__(self, env, action):
       flag=True
      # if(ambient.getPlacementMap().notValidOrientation(action.getOrient())):
       #    flag=False  
       return flag 
      
class SpeakToAllActionRuleFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.BroadcastAction)
        
    
    def __call__(self, env, action):
       flag=True
       return flag
                     
class ForwardActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.ForwardMoveMentAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())  
        
class TurnLeftActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.MoveLeftAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())     
       
class TurnRightActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.MoveRightAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())             
       
class CleanActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.CleanDirtAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())           
     
class DropActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.DropDirtAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient()) 
class SpeakActionExecuteFactory(Rule):
    
    def __init__(self):
        super().__init__(vwaction.SpeakAction)
        
    
    def __call__(self, env, action):
        action.execute(env)          
        
class SpeakToAllActionExecuteFactory(Executor):
    
    def __init__(self):
        super().__init__(vwaction.BroadcastAction)
        
    
    def __call__(self, env, action):
    
       
        action.execute(env)       
        
class Move(Executor):
    
    def __init__(self, agentmind):
        super().__init__(vwaction.ForwardMoveMentAction)
        act=vwaction.ForwardMoveMentAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class TurnLeft(Executor):
    
    def __init__(self, agentmind):
         super().__init__(vwaction.MoveLeftAction)
         act=vwaction.MoveLeftAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
         for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        

class TurnRight(Executor):
    
    def __init__(self, agentmind):
        super().__init__(vwaction.MoveRightAction)
        act=vwaction.MoveRightAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class CleanDirt(Executor):
    
    def __init__(self, agentmind):
        super().__init__(vwaction.CleanDirtAction)
        act=vwaction.CleanDirtAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class DropDirt(Executor):
    
    def __init__(self, agentmind):
        super().__init__(vwaction.DropDirtAction)
        act=vwaction.DropDirtAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
               
                
class Speak(Executor):
    
    def __init__(self, agentmind,receiver,message):
        super().__init__(vwaction.SpeakAction)
        act=vwaction.SpeakAction(agentmind.getName(),receiver,message)
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)                
class SpeakToAll(Executor):
    
    def __init__(self, agentmind,message):
        super().__init__(vwaction.BroadcastAction)
        act=vwaction.BroadcastAction(agentmind.getName(),message)
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)    
                       
        