from pystarworlds.Action import Action

from GridPerception import Message
from vwc import coord,colour,direction,location
import random


class PhysicalAction(Action):
     def __init__(self,ag,coord1):
      super().__init__(ag)  
      self.__currentcoord__=coord(coord1.x,coord1.y)
     def getCoordinate(self):
        return self.__currentcoord__

    
class CommunicationAction(Action):
    pass
class SensingAction(Action):
    pass

    
class ForwardMoveMentAction(PhysicalAction):
 
    def __init__(self,ag,coord1, orient):
        super().__init__(ag,coord1)
        
       
        
        coord2=self.getFrontCoordinate(coord1,orient)
        
        self.__newcoord__=coord(coord2.x,coord2.y)
    
  
    def getnewCoordinate(self):
        return self.__newcoord__
    
    def execute(self, ambient):
        
        pm=ambient.getPlacementMap()
        for i in range(pm.dim):
         for j in range(pm.dim):
           agentlocation=pm.state[coord(j,i)] 
           if(agentlocation.agent):
              if(agentlocation.agent.name==self.getActor()):
              
               
                
                  pm.replace_agent((self.__newcoord__.x,self.__newcoord__.y), agentlocation.agent)
                  pm.replace_agent((self.__currentcoord__.x,self.__currentcoord__.y), None)
      
           
    
    def isSame(self, action):
        if (type(self)==type(action)):
           return  self.getnewCoordinate()==action.getnewCoordinate()
        else:
           return False 
     
        
    def getFrontCoordinate(self,co,orientation):
    
     if (orientation=="east"):
      co2=coord(co.x+1,co.y)
     elif (orientation=="west"):
      co2=coord(co.x-1,co.y)
     elif (orientation=="south"):
      co2=coord(co.x,co.y+1)
     else:   #north
      co2=coord(co.x,co.y-1)
     #print(co2) 
     return co2          


class ChangeOrientationAction(PhysicalAction):
 
    def __init__(self,ag1,coord1,orient):
        super().__init__(ag1,coord1)
   
        self.__orient__=orient
       
        
      
    def getOrient(self):
        return self.__orient__
   
    def execute(self, ambient):
        
        pm=ambient.getPlacementMap()
        for i in range(pm.dim):
         for j in range(pm.dim):
           agentlocation=pm.state[coord(j,i)] 
           if(agentlocation.agent):
              if(agentlocation.agent.name==self.getActor()):
                pm.turn_agent(self.getOrient())

    def isSame(self, action):
        if (type(self)==type(action)):
         return  self.getOrient()==action.getOrient()
        else:
         return False

             


class MoveLeftAction(ChangeOrientationAction):
 
    def __init__(self,ag1,coord,orient):
        super().__init__(ag1,coord,orient)
   
    def execute(self, ambient):
        direct='east'
        if self.__orient__=='east':
          direct='north'   
        elif self.__orient__=='north':
          direct='west'   
        elif self.__orient__=='west':
          direct='south'   
        elif self.__orient__=='south':
          direct='east'   
        pm=ambient.getPlacementMap()
        for i in range(pm.dim):
         for j in range(pm.dim):
           agentlocation=pm.state[coord(j,i)] 
           if(agentlocation.agent):
              if(agentlocation.agent.name==self.getActor()):
                 pm.turn_agent(coord(j,i),direct)
    def isSame(self, action):
        if (type(self)==type(action)):
         return  self.getOrient()==action.getOrient()
        else:
         return False
      
class MoveRightAction(ChangeOrientationAction):
 
    def __init__(self,ag1,coord,orient):
        super().__init__(ag1,coord,orient)
       
    def execute(self, ambient):
       direct='east'
       if self.__orient__=='east':
          direct='south'   
       elif self.__orient__=='south':
          direct='west'   
       elif self.__orient__=='west':
          direct='north'   
       elif self.__orient__=='north':
          direct='east'   
       pm=ambient.getPlacementMap()
       for i in range(pm.dim):
         for j in range(pm.dim):
           agentlocation=pm.state[coord(j,i)] 
           if(agentlocation.agent):
              if(agentlocation.agent.name==self.getActor()):
                 pm.turn_agent(coord(j,i),direct)  
    
    def isSame(self, action):
        if (type(self)==type(action)):
         return  self.getOrient()==action.getOrient()
        else:
         return False
      
       
    
class NoMoveMentAction(Action):
 
    def __init__(self,):
        super().__init__("")
       
    def isSame(self, action):
       if (type(self)==type(action)):
        return True   
    def execute(self, ambient):
        print("No action")
        
        
  
class CleanDirtAction(PhysicalAction):
 
    def __init__(self,ag,coord,orient):
        super().__init__(ag,coord)
        
     
       
    def isSame(self, action):
        if (type(self)==type(action)):
          return  ((super().getActor()==action.getActor()))
        else:
          return False    
   
  
   
    def execute(self, ambient):
       
       pm=ambient.getPlacementMap()
       for i in range(pm.dim):
         for j in range(pm.dim):
           loc=pm.state[coord(j,i)] 
           if(loc.agent):
              if(loc.agent.name==self.getActor()):
                 pm.replace_dirt((super().getCoordinate().x,super().getCoordinate().y),None)
                 
                 print("Cleaned dirt")            
        
        
class DropDirtAction(PhysicalAction):
 
    def __init__(self,ag,coord,orient):
        super().__init__(ag,coord)
     
    
    def isSame(self, action):
        if (type(self)==type(action)):
          return  ((super().getActor()==action.getActor()))
        else:
          return False    
   
  
   
    def execute(self, ambient):
     print("IN DROP DIRT")  
     pm=ambient.getPlacementMap()
     for i in range(pm.dim):
         for j in range(pm.dim):
           loc=pm.state[coord(j,i)] 
           if(loc.agent):
              if(loc.agent.name==self.getActor()):
                
               n=random.randint(1,3) 
               if(n==1):   
                pm.replace_dirt((super().getCoordinate().x,super().getCoordinate().y), 'orange')
               else:
                pm.replace_dirt((super().getCoordinate().x,super().getCoordinate().y), 'green')
                   
          
class SpeakAction(CommunicationAction):
 
    def __init__(self,sender,receiver,message):
        super().__init__(sender)
        self.__receiver__=receiver
        self.__message__=message
   
   
    def getSender(self):
        return self.getActor()
   
    def getReceiver(self):
        return self.__receiver__
    def getMessage(self):
        return self.__message__
    
    
    def isSame(self, action):
        if (type(self)==type(action)):
         return  ((super().getActor()==action.getActor())and(self.receiver==action.getReceiver())and (self.message==action.getMessage()) )
        else:
         return False    
    
    def execute(self, env):  # environment reference reqired here
      
       per=Message(self.getSender(),self.getReceiver(),self.getMessage())
       env.getPhysics().notifySinglePerception(per)
      
        
       
       
class BroadcastAction(CommunicationAction):
 
  def __init__(self,sender,message):
       super().__init__(sender)
       self.__message__=message 
  def getSender(self):
        return self.getActor()
   
  def getMessage(self):
        return self.__message__
    
   
   
    
  def isSame(self, action):
       if (type(self)==type(action)):
          return  ((super().getMessage()==action.getMessage()) )
       else:
          return False    
    
  def execute(self, env):  # environment reference reqired here
      

        
       for a in env.getAmbient().getAgents(): 
         per=Message(self.getSender(),a.getName(),self.getMessage())
         env.getPhysics().notifySinglePerception(per)
         print(a.getName())  