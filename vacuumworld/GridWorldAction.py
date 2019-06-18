from BasicBuildingBlock.Action import Action
from GridWorld.EntityType import CellType,AgentColor,DirtColor
from GridWorld.Orientation_Direction import Orientation
class PhysicalAction(Action):
   def is_possible(self,acts):
        
    for a in acts:
     if(a.isCompatible(self)):
        return True
    return False 
   
    pass
class CommunicationAction(Action):
    pass
class SensingAction(Action):
    pass

    
class ForwardMoveMentAction(PhysicalAction):
 
    def __init__(self,ag,coord, coord2):
        super().__init__(ag)
        
        self.__currentcoord__=coord
        self.__newcoord__=coord2
    
    def getcurrentCoordinate(self):
        return self.__currentcoord__

    def getnewCoordinate(self):
        return self.__newcoord__
    
    def execute(self, pm):
        
        pm.placeEntity(self.getnewCoordinate(),self.getActor(),pm.getEntityType(self.getActor()),pm.getOrientation(self.getActor()),pm.getAgentColor(self.getcurrentCoordinate()))
        pm.makeVacant(self.getcurrentCoordinate())   
    
    def isSame(self, action):
        if (type(self)==type(action)):
           return  self.getnewCoordinate()==action.getnewCoordinate()
        else:
           return False 
     
        
             


class ChangeOrientationAction(PhysicalAction):
 
    def __init__(self,ag1,orient):
        super().__init__(ag1)
   
        self.__orient__=orient
       
        
      
    def getOrient(self):
        return self.__orient__
   
    def execute(self, pm):
        
        pm.changeOrientation(super().getActor(),self.__orient__)

    def isSame(self, action):
        if (type(self)==type(action)):
         return  self.getOrient()==action.getOrient()
        else:
         return False

             


class MoveLeftAction(ChangeOrientationAction):
 
    def __init__(self,ag1,orient):
        super().__init__(ag1,orient)
   

        
      
  
   
    def execute(self, pm):
        if self.__orient__== Orientation.EAST:
           self.__orient__=Orientation.NORTH
        elif self.__orient__== Orientation.NORTH:
           self.__orient__=Orientation.WEST
        elif self.__orient__== Orientation.WEST:
           self.__orient__=Orientation.SOUTH
        elif self.__orient__== Orientation.SOUTH:
           self.__orient__=Orientation.EAST        
      
        
        pm.changeOrientation(super().getActor(),self.__orient__)

    def isSame(self, action):
        if (type(self)==type(action)):
         return  self.getOrient()==action.getOrient()
        else:
         return False
      
class MoveRightAction(ChangeOrientationAction):
 
    def __init__(self,ag1,orient):
        super().__init__(ag1,orient)
       
        
      
  
   
    def execute(self, pm):
        if self.__orient__== Orientation.EAST:
           self.__orient__=Orientation.SOUTH
        elif self.__orient__== Orientation.SOUTH:
           self.__orient__=Orientation.WEST        
        elif self.__orient__== Orientation.WEST:
           self.__orient__=Orientation.NORTH
        elif self.__orient__== Orientation.NORTH:
           self.__orient__=Orientation.EAST
        
        
        pm.changeOrientation(super().getActor(),self.__orient__)

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
        
        
  
class CleanAction(PhysicalAction):
 
    def __init__(self,ag,coord):
        super().__init__(ag)
        self.__currentcoord__=coord
    
    def getCoordinate(self):
        return self.__currentcoord__
     
       
    def isSame(self, action):
        if (type(self)==type(action)):
          return  ((super().getActor()==action.getActor()))
        else:
          return False    
   
  
   
    def execute(self, pm):
      pm.cleanDirt(self.getCoordinate())
        
        
class DropAction(PhysicalAction):
 
    def __init__(self,ag,coord,color):
        super().__init__(ag)
        self.__currentcoord__=coord
        self.__dirtcolor__=color
    
        
    def getCurrentCoordinates(self):
        return self.__currentcoord__
    
    def isSame(self, action):
        if (type(self)==type(action)):
          return  ((super().getActor()==action.getActor()))
        else:
          return False    
   
  
   
    def execute(self, pm):
      pm.placeEntity(self.getCurrentCoordinates(),self.getActor(),CellType.USERONDIRT,pm.getOrientation(self.getActor()),self.color)
          
          
class SpeakAction(CommunicationAction):
 
    def __init__(self,sender,receiver,message):
        super().__init__(sender)
        self.__receiver__=receiver
        self.__message__=message
   
   
    def geSender(self):
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
    
    def execute(self, env):
        env.notifyActuator(self)


class BroadcastAction(SpeakAction):
 
    def __init__(self,sender,message):
        super().__init__(sender,None,message)
        
   
   
    def getReceiver(self):
        return None   
    
    
    def isSame(self, action):
        if (type(self)==type(action)):
          return  ((super().getMessage()==action.getMessage()) )
        else:
          return False    
    
  
          