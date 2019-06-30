# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:34:00 2019

@author: PDAC004
"""


####################################################
class VWGridPerceptionFactory(PerceptionFactory):
    
    def __init__(self):
        super().__init__(Observation)
        
    
    def __call__(self, env, agent,s):
        if(s.getOwner()==(agent.getID())):
           return Observation(agent.getID(), env.getAmbient())            
       
class ForwardActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(ForwardMoveMentAction)
        
    
    def __call__(self, env, action):
       flag=True
       if(env.getAmbient().getPlacementMap().isOutsideGrid(action.getnewCoordinate())):
         flag=False
       elif(env.getAmbient().getPlacementMap().isOccupiedByActor(action.getnewCoordinate())): 
         flag=False
        
       return flag             
       
class TurnLeftActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(MoveLeftAction)
        
    
    def __call__(self, env, action):
       flag=True
      # if(ambient.getPlacementMap().notValidOrientation(action.getOrient())):
       #    flag=False  
       return flag             
       
class TurnRightActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(MoveRightAction)
        
    
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
      
    
    
class CleanActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(CleanDirtAction)
        
    
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
class DropActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(DropDirtAction)
        
    
    def __call__(self, env, action):
       flag=True
       if(env.getAmbient().getPlacementMap().notValidOrientation(action.getOrient())):
           flag=False  
       return flag             
class SpeakActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(SpeakAction)
        
    
    def __call__(self, env, action):
       flag=True
      # if(ambient.getPlacementMap().notValidOrientation(action.getOrient())):
       #    flag=False  
       return flag       
class SpeakToAllActionRuleFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(BroadcastAction)
        
    
    def __call__(self, env, action):
       flag=True
               
       return flag                     
class ForwardActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(ForwardMoveMentAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())  
        
class TurnLeftActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(MoveLeftAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())     
       
class TurnRightActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(MoveRightAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())             
       
class CleanActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(CleanDirtAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient())           
     
class DropActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(DropDirtAction)
        
    
    def __call__(self, env, action):
        action.execute(env.getAmbient()) 
class SpeakActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(SpeakAction)
        
    
    def __call__(self, env, action):
        action.execute(env)          
        
class SpeakToAllActionExecuteFactory(RuleFactory):
    
    def __init__(self):
        super().__init__(BroadcastAction)
        
    
    def __call__(self, env, action):
    
       
        action.execute(env)       
        
class Move(ActionFactory):
    
    def __init__(self, agentmind):
        super().__init__(ForwardMoveMentAction)
        act=ForwardMoveMentAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class TurnLeft(ActionFactory):
    
    def __init__(self, agentmind):
         super().__init__(MoveLeftAction)
         act=MoveLeftAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
         for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        

class TurnRight(ActionFactory):
    
    def __init__(self, agentmind):
        super().__init__(MoveRightAction)
        act=MoveRightAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class CleanDirt(ActionFactory):
    
    def __init__(self, agentmind):
        super().__init__(CleanDirtAction)
        act=CleanDirtAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
        
class DropDirt(ActionFactory):
    
    def __init__(self, agentmind):
        super().__init__(DropDirtAction)
        act=DropDirtAction(agentmind.getName(),agentmind.getBody().getCoordinate(),agentmind.getBody().getOrientation())
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)
                
class Speak(ActionFactory):
    
    def __init__(self, agentmind,receiver,message):
        super().__init__(SpeakAction)
        act=SpeakAction(agentmind.getName(),receiver,message)
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)                
class SpeakToAll(ActionFactory):
    
    def __init__(self, agentmind,message):
        super().__init__(BroadcastAction)
        act=BroadcastAction(agentmind.getName(),message)
        for ac in agentmind.getBody().getActuators():
            if(ac.isCompatible(act)):
                ac.attempt(act)    
                       
        