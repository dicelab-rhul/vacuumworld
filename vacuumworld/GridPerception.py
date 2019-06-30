# -*- coding: utf-8 -*-
from pystarworlds.Perception import Perception
from Coordinate import Coordinate
from Orientation_Direction import Orientation
from collections import namedtuple
from EntityType import CellType, AgentColor,DirtColor
from vw import PhysicalAllocationMap

from vwc import coord,colour,location,agent,observation




class VisionPerception(Perception):
  def __init__(self,agid,ambient):  # id of agent sent not full agent
      super().__init__(agid)
      
      pm=ambient.getPlacementMap()
      for i in range(pm.dim):
            for j in range(pm.dim):
               agentlocation=pm.state[coord(j,i)]
               if(agentlocation.agent):
                   if(agentlocation.agent.name==agid):
                    self.__coordinate__=agentlocation.coordinate
                    self.__orientation__ = agentlocation.agent.direction
                    self.__color__=agentlocation.agent.colour

  def getOrientation(self):
     return self.__orientation__
  def getCoordinates(self):
     return self.__coordinate__
  def getColor(self):
     return self.__color__
  
    
      
class GridVisionPerception(VisionPerception):
     def __init__(self,agid,ambient):  # id of agent sent not full agent
       super().__init__(agid,ambient)
       
     
class Observation(GridVisionPerception):
    def __init__(self,agid,ambient):  # id of agent sent not full agent
       super().__init__(agid,ambient)
       self.perceptionGrid={}
       self.observation=None
       pm=ambient.getPlacementMap()
       for i in range(pm.dim):
            for j in range(pm.dim):
               location=pm.state[coord(j,i)]
               if(location.agent):
                  if(location.agent.name==agid):
                     
                     center=location
                     wall=pm.isOutsideGrid(center.coordinate)
                     self.perceptionGrid["own"]= center
                    # self.observation.own=location
                    
                     tcoord=self.getFrontCoordinate(center.coordinate,center.agent.direction)
                     print(tcoord)
                     wall=pm.isOutsideGrid(tcoord)
                     if(wall):
                       location=None
                     else:
                       location=pm.state[tcoord]
                         
                     self.perceptionGrid["front"]=location
                     #self.observation.front.location=location
                 
                     
                     
                     
                     tcoord=self.getLeftCoordinate(center.coordinate,center.agent.direction)
                     wall=pm.isOutsideGrid(tcoord)
                     if(wall):
                       location=None
                     else:
                       location=pm.state[tcoord]
                     self.perceptionGrid["left"]=location
#                     observation.left=location
                 
                     
                     
                     
                     tcoord=self.getRightCoordinate(center.coordinate,center.agent.direction)
                     wall=pm.isOutsideGrid(tcoord)
                     if(wall):
                       location=None
                     else:
                       location=pm.state[tcoord]
                     
                     self.perceptionGrid["right"]=location
                #     self.observation.right=location
                 
                     
                     
                     tcoord=self.getFrontLeftCoordinate(center.coordinate,center.agent.direction)
                     wall=pm.isOutsideGrid(tcoord)
                     if(wall):
                       location=None
                     else:
                       location=pm.state[tcoord]
                     
                     self.perceptionGrid["frontleft"]=location#,wall)
                  #   self.observation.frontleft=location
                  
                     
                     tcoord=self.getFrontRightCoordinate(center.coordinate,center.agent.direction)
                     wall=pm.isOutsideGrid(tcoord)
                     if(wall):
                       location=None
                     else:
                       location=pm.state[tcoord]
                     
                     self.perceptionGrid["frontright"]=location#,wall)
                 #    self.observation.frontright=location
       self.observation=observation(self.perceptionGrid['own'],self.perceptionGrid['left'],self.perceptionGrid['right'],self.perceptionGrid['front'],self.perceptionGrid['frontleft'],self.perceptionGrid['frontright'])             
     #  print(self.perceptionGrid)           
##################################################### def getFrontCoordinate(self,co,orientation):
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
    def getLeftCoordinate(self,co,orientation):
    
     if (orientation=="east"):
      co2=coord(co.x,co.y-1)
     elif (orientation=="west"):
      co2=coord(co.x,co.y+1)
     elif (orientation=="south"):
      co2=coord(co.x+1,co.y)
     else:   #north
      co2=coord(co.x-1,co.y)
     #print(co2) 
     return co2

    def getRightCoordinate(self,co,orientation):
    
     if (orientation=="east"):
      co2=coord(co.x,co.y+1)
     elif (orientation=="west"):
      co2=coord(co.x,co.y-1)
     elif (orientation=="south"):
      co2=coord(co.x-1,co.y)
     else:   #north
      co2=coord(co.x+1,co.y)
     return co2
    def getFrontRightCoordinate(self,co,orientation):
    
     
     if (orientation=="east"):
      co2=coord(co.x+1,co.y+1)
     elif (orientation=="west"):
      co2=coord(co.x-1,co.y-1)
     elif (orientation=="south"):
      co2=coord(co.x+1,co.y-1)
     else:   #north
      co2=coord(co.x-1,co.y+1)
   
     return co2
 
    def getFrontLeftCoordinate(self,co,orientation):
    
     if (orientation=="east"):
      co2=coord(co.x+1,co.y-1)
     elif (orientation=="west"):
      co2=coord(co.x-1,co.y+1)
     elif (orientation=="south"):
      co2=coord(co.x+1,co.y+1)
     else:   #north
      co2=coord(co.x-1,co.y-1)
     return co2     
    
    def getID(self,t):
         g=self.perceptionGrid[t] 
         return g.location.agent.name
  
    def getCoordinate(self,t):
         g=self.perceptionGrid[t] 
         return g.location.coordinate
     
   
 
class Message(Perception):
 
    def __init__(self,sender,receiver,message):
        super().__init__(receiver)
      
        self.__sender__=sender
        self.__message__=message
   
   
   
    def getSender(self):
        return self.__sender__
    def getMessage(self):
        return self.__message__
    
class ActionResultPerception(Perception):
    
    def __init__(self,agid,action,result):
        super().__init__(agid)
        self.__actionAttempted__=action
        self.__result__=result   
     
    def getResult(self):
        return self.__result__
    
    def getActionAttempted(self):
        return self.__actionAttempted__
    