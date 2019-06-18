# -*- coding: utf-8 -*-
from BasicBuildingBlock.Perception import Perception
from BasicBuildingBlock.Coordinate import Coordinate
from GridWorld.Orientation_Direction import Orientation
from collections import namedtuple
from GridWorld.EntityType import CellType, AgentColor,DirtColor


class VisionPerception(Perception):
  def __init__(self,agid,allocationmap):  # id of agent sent not full agent
      super().__init__(agid)
      self.__coordinate__=allocationmap.getCoordinate(agid)
      self.__orientation__ = allocationmap.getOrientation(agid)
      self.__color__=allocationmap.getColor(agid)

  def getOrientation(self):
     return self.__orientation__
  def getCoordinates(self):
     return self.__coordinate__
  def getColor(self):
     return self.__color__

  
  def isOrientationNorth(self):
      if(self.__orientation__==Orientation.NORTH):
          return True
      else:
          return False
  def isOrientationSouth(self):
      if(self.__orientation__==Orientation.SOUTH):
          return True
      else:
          return False 
  def isOrientationWest(self):
      if(self.__orientation__==Orientation.WEST):
          return True
      else:
          return False  
  def isOrientationEast(self):
      if(self.__orientation__==Orientation.EAST):
          return True
      else:
          return False
  def isOwnColorGreen(self):
      if(self.__color__==AgentColor.GREEN):
          return True
      else:
          return False
  def isOwnColorOrange(self):
      if(self.__color__==AgentColor.ORANGE):
          return True
      else:
          return False    
  def isOwnColorWhite(self):
      if(self.__color__==AgentColor.WHITE):
          return True
      else:
          return False
      
class GridVisionPerception(VisionPerception):
     def __init__(self,agid,allocationmap):  # id of agent sent not full agent
       super().__init__(agid,allocationmap)
       
     
class VWGridVisionPerception(GridVisionPerception):
     def __init__(self,agid,fullgrid):  # id of agent sent not full agent
       super().__init__(agid,fullgrid)
       self.__perceptionGrid__={}
       eid=super().getOwner()
       co=super().getCoordinates() 
       orient=super().getOrientation()
       ctype=fullgrid.getCellTypeOnCoord(co)
       color=super().getColor()
       self.__perceptionGrid__["center"]= self.getOwnCellPerception(eid,co,orient,ctype,color,fullgrid)  
       leftcoord=fullgrid.getLeftCoordinate(co,orient)
       self.__perceptionGrid__["left"]= self.getCellPerception(leftcoord,fullgrid)
       frontlcoord=fullgrid.getFrontLeftCoordinate(co,orient)
       self.__perceptionGrid__["frontleft"] =self.getCellPerception(frontlcoord,fullgrid) 
       frontcoord=fullgrid.getFrontCoordinate(co,orient)
       self.__perceptionGrid__["front"]=self.getCellPerception(frontcoord,fullgrid) 
       frontrcoord=fullgrid.getFrontRightCoordinate(co,orient)
       self.__perceptionGrid__["frontright"]=self.getCellPerception(frontrcoord,fullgrid) 
       rightcoord=fullgrid.getRightCoordinate(co,orient)
       self.__perceptionGrid__["right"] =self.getCellPerception(rightcoord,fullgrid)
 
      # print(self.perceptionGrid)
     
     def getOwnCellPerception(self,entityid,co,orient,ctype,color,fullgrid):
         if ctype == CellType.AGENT:
              return [CellType.AGENT,co,entityid,orient,color,None]
         elif ctype == CellType.USER:
              return [CellType.USER,co,entityid,orient,None,None]
         elif ctype == CellType.AGENTONDIRT:
              return [CellType.AGENTONDIRT,co,entityid,orient,color,fullgrid.getDirtColor(co)]
         elif ctype == CellType.USERONDIRT:
              return [CellType.USERONDIRT,co,entityid,orient,None,fullgrid.getDirtColor(co)]
         else:
              print("-----------")
              #raise ValueError("Not valid")  
     def getCellPerception(self,co,fullgrid):
         if(fullgrid.notValidCoordinate(co)):
             return [CellType.WALL,co,None,None,None,None] 
             #raise ValueError("Not valid coordinate")  
         else:       
          etype=fullgrid.getCellTypeOnCoord(co)
          
         
          if(etype==CellType.AGENT):
            entityid=fullgrid.getEntityID(co)
            color=fullgrid.getAgentColor(co)
            orient=fullgrid.getEntityOrientation(co)  
            return [CellType.AGENT,co,entityid,orient,color,None]
          elif(etype==CellType.USER):
             entityid=fullgrid.getEntityID(co)
             orient=fullgrid.getEntityOrientation(co)  
             return [CellType.USER,co,entityid,orient,None,None]
          elif(etype==CellType.DIRT):   
             color=fullgrid.getDirtColor(co)
             return [CellType.DIRT,co,None,None,None,color]
             
          elif(etype==CellType.AGENTONDIRT):
           
            entityid=fullgrid.getEntityID(co)
            color=fullgrid.getAgentColor(co)
            colord=fullgrid.getDirtColor(co)
            orient=fullgrid.getEntityOrientation(co)  
            return [CellType.AGENTONDIRT,co,entityid,orient,color,colord]
      
          elif(etype==CellType.USERONDIRT):
            entityid=fullgrid.getEntityID(co)
            colord=fullgrid.getDirtColor(co)
            orient=fullgrid.getEntityOrientation(co)  
            return [CellType.USERONDIRT,co,entityid,orient,None,colord]
      
          elif(etype==CellType.EMPTY):
              return [CellType.EMPTY,co,None,None,None,None]
          else:
             
              print(etype)
              #raise ValueError("Not valid")  
         
        
      

     def getID(self,t):
         g=self.__perceptionGrid__[t] 
         return g[2]
     def getCellType(self,t):
         g=self.__perceptionGrid__[t] 
         return g[0]
 
     def getCoordinate(self,t):
         g=self.__perceptionGrid__[t] 
         return g[1]
     
     def isEmptyLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"]
        if left[0]==CellType.EMPTY:
          return True
        else: 
          return False
     def isEmptyRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if right[0]==CellType.EMPTY:
          return True
        else: 
          return False
     def isEmptyForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if front[0]==CellType.EMPTY:
          return True
        else: 
          return False
     def isEmptyForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if left[0]==CellType.EMPTY:
          return True
        else: 
          return False
     def isEmptyForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if right[0]==CellType.EMPTY:
          return True
        else: 
          return False
     
     def isAgentLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.AGENT or  left[0]==CellType.AGENTONDIRT):
         return True
        else:           
         return False
     def isAgentRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.AGENT or  right[0]==CellType.AGENTONDIRT):
          return True
        else:           
         return False
     def isAgentForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.AGENT or  front[0]==CellType.AGENTONDIRT):
         return True
        else:           
         return False
     def isAgentForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.AGENT or  left[0]==CellType.AGENTONDIRT):
          return True
        else:           
         return False
     def isAgentForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.Agent or  right[0]==CellType.AgentOnDirt):
          return True
        else:           
         return False

     def isUserLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.USER or left[0]==CellType.USERONDIRT):
         return True
        else:           
         return False
     def isUserRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.USER or right[0]==CellType.USERONDIRT):
          return True
        else:           
         return False
     def isUserForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.USER or front[0]==CellType.USERONDIRT):
         return True
        else:           
         return False
     def isUserForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.USER or left[0]==CellType.USERONDIRT):
          return True
        else:           
         return False
     def isUserForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.USER or right[0]==CellType.USERONDIRT):
          return True
        else:           
         return False
     def isDirtLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.DIRT or left[0]==CellType.AGENTONDIRT or left[0]==CellType.USERONDIRT):
         return True
        else:           
         return False
     def isDirtRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.DIRT or right[0]==CellType.AGENTONDIRT or right[0]==CellType.USERONDIRT):
          return True
        else:           
         return False
     def isDirtForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.DIRT or front[0]==CellType.AGENTONDIRT or front[0]==CellType.USERONDIRT):
           return True
        else:           
           return False
     def isDirtForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.DIRT or left[0]==CellType.AGENTONDIRT or left[0]==CellType.USERONDIRT):
            return True
        else:           
         return False
     def isDirtForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.DIRT or right[0]==CellType.AGENTONDIRT or right[0]==CellType.USERONDIRT):
             return True
        else:           
         return False
     def isActorLeft(self):
      return  self.isUserLeft() or self.isAgentLeft() 
     def isActorRight(self):
      return  self.isUserRight() or self.isAgentRight() 
     def isActorForward(self):
      return  self.isUserForward() or self.isAgentForward() 
     def isActorForwardLeft(self):
      return  self.isUserForwardLeft() or self.isAgentForwardLeft() 
     def isActorForwardRight(self):
      return  self.isUserForwardRight() or self.isAgentForwardRight() 
     def isWallForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.WALL):
         return True
        else:           
         return False
     def isWallLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.WALL):
          return True
        else:           
         return False
     def isWallRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.WALL):
         return True
        else:           
         return False
     def getAgentLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.AGENT or  left[0]==CellType.AGENTONDIRT):
         return left[2]
        else:           
         return None
     def getAgentRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.AGENT or  right[0]==CellType.AGENTONDIRT):
          return right[2]
        else:           
          return None
     def getAgentForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.AGENT or  front[0]==CellType.AGENTONDIRT):
         return front[2]
        else:           
         return None
     def getAgentForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.AGENT or  left[0]==CellType.AGENTONDIRT):
          return left[2]
        else:           
         return None
     def getAgentForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.AGENT or  right[0]==CellType.AGENTONDIRT):
           return right[2]
        else:           
           return None 
     def getUserLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.USER or left[0]==CellType.USERONDIRT):
         return left[2]
        else:           
         return None
     def getUserRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.USER or right[0]==CellType.USERONDIRT):
          return right[2]
        else:           
         return None
     def getUserForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.USER or front[0]==CellType.USERONDIRT):
         return front[2]
        else:           
         return None
     def getUserForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.USER or left[0]==CellType.USERONDIRT):
          return left[2]
        else:           
         return None
     def getUserForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.USER or right[0]==CellType.USERONDIRT):
          return right[2]
        else:           
         return None
     def getActorLeft(self):
      if(self.isUserLeft()):
        self.getUserLeft()
      elif( self.isAgentLeft()):
        self.getAgentLeft()
      else:
        return None
    
     def getActorRight(self):
      if(self.isUserRight()):
        self.getUserRight()
      elif( self.isAgentRight()):
        self.getAgentRight()
      else:
        return None
     def getActorForward(self):
      if(self.isUserForward()):
        self.getUserForward()
      elif( self.isAgentForward()):
        self.getAgentForward()
      else:
        return None
     def getActorForwardLeft(self):
      if(self.isUserForwardLeft()):
        self.getUserForwardLeft()
      elif( self.isAgentForwardLeft()):
        self.getAgentForwardLeft()
      else:
        return None
     def getActorForwardRight(self):
      if(self.isUserForwardRight()):
        self.getUserForwardRight()
      elif( self.isAgentForwardRight()):
        self.getAgentForwardRight()
      else:
        return None
      
     def getDirtLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        if(left[0]==CellType.DIRT or left[0]==CellType.AGENTONDIRT or left[0]==CellType.USERONDIRT):
          return left[5] 
        else:           
         return None
     def getDirtRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        if(right[0]==CellType.DIRT or right[0]==CellType.AGENTONDIRT or right[0]==CellType.USERONDIRT):
          return right[5] 
        else:           
         return None
     def getDirtForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        if(front[0]==CellType.DIRT or front[0]==CellType.AGENTONDIRT or front[0]==CellType.USERONDIRT):
          return front[5] 
        else:           
         return None
     def getDirtForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        if(left[0]==CellType.DIRT or left[0]==CellType.AGENTONDIRT or left[0]==CellType.USERONDIRT):
          return left[5] 
        else:           
         return None
     def getDirtForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        if(right[0]==CellType.DIRT or right[0]==CellType.AGENTONDIRT or right[0]==CellType.USERONDIRT):
          return right[5] 
        else:           
         return None
     def getCoordinatesLeft(self):
        left=[]
        left=self.__perceptionGrid__["left"] 
        return left[1]
     def getCoordinatesRight(self):
        right=[]
        right=self.__perceptionGrid__["right"] 
        return right[1]
     def getCoordinatesForward(self):
        front=[]
        front=self.__perceptionGrid__["front"] 
        return front[1]
     def getOwnCoordinates(self):
        front=[]
        front=self.__perceptionGrid__["center"] 
        return front[1]
     def getOwnColor(self):
        front=[]
        front=self.__perceptionGrid__["center"] 
        
        return front[4]
     def amIWhiteAgent(self):
       # print("---------- agent color------------")
       # print(self.getOwnColor())
        if(self.getOwnColor()==AgentColor.WHITE):
           return True
        else: 
           return False
     def amIGreenAgent(self):
        if(self.getOwnColor()==AgentColor.GREEN):
           return True
        else: 
           return False
     def amIOrangeAgent(self):
        if(self.getOwnColor()==AgentColor.ORANGE):
           return True
        else: 
           return False
     def amICleaningAgent(self):
         return self.amIGreenAgent() or self.amIOrangeAgent() or self.amIWhiteAgent()  
     def canMoveForward(self):
         if self.isActorForward() or self.isWallForward():
          #   print("Cannot move")
             return False
         else:
             return True
         
         
         
     def getDirtColorIamSittingOn(self):
         return self.getDirtColor("center")
         
     def iamSittingOnGreenDirt(self):
         if self.getDirtColor("center")== DirtColor.GREEN:
             return True
         else:
              return False
     def iamSittingOnOrangeDirt(self):
         if self.getDirtColor("center")== DirtColor.ORANGE:
             return True
         else:
              return False
     def amISittingOnDirt(self):
        # print(self.iamSittingOnGreenDirt() or self.iamSittingOnOrangeDirt())
         return self.iamSittingOnGreenDirt() or self.iamSittingOnOrangeDirt()
         
         
     def getDirtColor(self,t):
        c=self.__perceptionGrid__[t] 
        return c[5]
       
     def getCoordinatesForwardLeft(self):
        left=[]
        left=self.__perceptionGrid__["frontleft"] 
        return left[1]

     def getCoordinatesForwardRight(self):
        right=[]
        right=self.__perceptionGrid__["frontright"] 
        return right[1]
    
    
     ####################################################################################
class VWCommunicationPerception(Perception):
 
    def __init__(self,sender,receiver,message):
        super().__init__(receiver)
      
        self.__sender__=sender
        self.__message__=message
   
   
   
    def getSender(self):
        return self.__sender__
    def getMessage(self):
        return self.__message__
    
class VWActionResultPerception(Perception):
    
    def __init__(self,agid,action,result):
        super().__init__(agid)
        self.__actionAttempted__=action
        self.__result__=result   
     
    def getResult(self):
        return self.__result__
    
    def getActionAttempted(self):
        return self.__actionAttempted__
    