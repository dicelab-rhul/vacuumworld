# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:35:53 2019

@author: PDAC004
"""

from BasicBuildingBlock.Identificaiton import Identifiable
from GridWorld.Orientation_Direction import Orientation

from BasicBuildingBlock.Coordinate import Coordinate


from tkinter import Button, Frame, Tk
from GridWorld.EntityType import CellType,AgentColor,DirtColor
import numpy as np

from PIL import Image, ImageTk
class PhysicalAllocationMap(Identifiable):
    
   def __init__(self,w,h):
    self.__grid__ = {}
    for x in range(w):
        for y in range(h):
         self.__grid__[(x,y)] = [CellType.EMPTY,None,None,None,None]
    
    self.__width__=w
    self.__height__=h
   def getWidthOfGrid(self):
      return self.__width__

   def getHeightOfGrid(self):
        return self.__height__
   def placeEntity(self, coord,entityid,Etype,orient,color):
       
      list1=self.__grid__[(coord.getX(),coord.getY())]
     
      if list1[0]==CellType.EMPTY: 
         if (Etype==CellType.AGENT): # if empty place 
            list1[0]=Etype
            list1[1]=entityid
            list1[2]=orient
            list1[3]=color
            list1[4]=None
            self.__grid__[(coord.getX(),coord.getY())]=list1
         elif Etype==CellType.USER: # if empty place 
            list1[0]=Etype
            list1[1]=entityid
            list1[2]=orient
            list1[3]=None
            list1[4]=None
            self.__grid__[(coord.getX(),coord.getY())]=list1
      
         elif Etype==CellType.DIRT: # if empty place 
            list1[0]=Etype
            list1[1]=None
            list1[2]=None
            list1[3]=None
            list1[4]=color
            self.__grid__[(coord.getX(),coord.getY())]=list1
      
      else:    # if occupied
       if(list1[0]==CellType.DIRT and Etype==CellType.AGENT):  # Agent can be placed on Dirt
         list1[0]=CellType.AGENTONDIRT
         list1[1]=entityid
         list1[2]=orient
         list1[3]=color
         self.__grid__[(coord.getX(),coord.getY())]=list1
       elif(list1[0]==CellType.DIRT and Etype==CellType.USER):  # Agent can be placed on Dirt
         list1[0]=CellType.USERONDIRT
         list1[1]=entityid
         list1[2]=orient
         list1[3]=color
         self.__grid__[(coord.getX(),coord.getY())]=list1
           
       elif(list1[0]==CellType.DIRT and Etype==CellType.DIRT): # no dirt cna be placed on dirt 
         raise ValueError("Dirt Can not be placed on another Dirt")   
       elif(list1[0]==CellType.AGENT and Etype==CellType.DIRT ): # nothing can be placed on agent
         raise ValueError("Dirt cannot be placed on Agent")   
       elif(list1[0]==CellType.AGENT and Etype==CellType.USER ): # nothing can be placed on agent
         raise ValueError("User cannot walk over Agent")   
       elif(list1[0]==CellType.AGENT and Etype==CellType.AGENT ): # nothing can be placed on agent
         raise ValueError("Agent cannot walk over Agent")   
       elif(list1[0]==CellType.USER and Etype==CellType.DIRT ): # nothing can be placed on agent
         raise ValueError("Dirt cannot be placed on User")   
       elif(list1[0]==CellType.USER and Etype==CellType.USER ): # nothing can be placed on agent
         raise ValueError("User cannot walk over user")   
       elif(list1[0]==CellType.USER and Etype==CellType.AGENT ): # nothing can be placed on agent
         raise ValueError("Agent cannot walk over User")   
       else:
         raise ValueError("Not possible action")   
     # print(self.grid)    
         
   def makeVacant(self,coord): 
    if(self.notValidCoordinate(coord)):
        raise ValueError("Not valid coordinate")     
    else:
      list1=self.__grid__[(coord.getX(),coord.getY())]
      if list1[0]==CellType.AGENT or list1[0]==CellType.USER or list1[0]==CellType.DIRT :  
         list1 = [CellType.EMPTY,None,None,None,None]
         self.__grid__[(coord.getX(),coord.getY())]=list1
      elif list1[0]==CellType.AGENTONDIRT or list1[0]==CellType.USERONDIRT :
         dcolor=list1[4]
         list1 = [CellType.DIRT, None,None,None,dcolor]
         self.__grid__[(coord.getX(),coord.getY())]=list1  
      else: 
         print("Cannot vacate this location")
   def cleanDirt(self,coord):    
    if(self.notValidCoordinate(coord)):
        raise ValueError("Not valid coordinate")     
    else:
      list1=self.__grid__[(coord.getX(),coord.getY())]
      if list1[0]==CellType.AGENTONDIRT :  
         list1[0] = CellType.AGENT
         list1[4]= None
         self.__grid__[(coord.getX(),coord.getY())]=list1  
       
       
   def notValidCoordinate(self,co):
     
    if(co.getX()>=self.getHeightOfGrid()):
      return True
    
    elif(co.getY()>=self.getWidthOfGrid()):
      return True
     
    elif((co.getY())<=-1):
        return True
     
    elif((co.getX())<=-1):
        return True
    else:
     return False
    
   def notValidOrientation(self,orient):
     for i in Orientation:
        if i==orient : 
           return False
     return True
   def isOccupiedByActor(self, coord):
     list1=self.__grid__[(coord.x,coord.y)]
     if(list1[0]==CellType.AGENT or list1[0]==CellType.AGENTONDIRT or list1[0]==CellType.USER or list1[0]==CellType.USERONDIRT ): 
            return True
     else:
            return False
    
    
   def getEntityID(self, coord):  
    
    if(self.notValidCoordinate(coord)):
    
     return None
    else:
     
     list1=self.__grid__[(coord.getX(),coord.getY())] 
     if(list1[0]==CellType.EMPTY):  #
       return  None
     elif (list1[0]==CellType.AGENTONDIRT or list1[0]==CellType.USERONDIRT or list1[0]==CellType.USER or list1[0]==CellType.AGENT):
       return list1[1]    
     else:
       return None
   def getCoordinate(self, entityid):
    
     for x in range(self.__width__):
        for y in range(self.__height__):
         list1=self.__grid__[(x,y)]
         if(list1[1]==entityid):
            return Coordinate(x,y) 
     return None
     raise ValueError("Not valid entity ID")   
     
   def getOrientation(self, entityid):
     for x in range(self.__width__):
        for y in range(self.__height__):
         list1=self.__grid__[(x,y)]
         if(list1[1]==entityid): 
            return list1[2]
     
     return None
   
   def getColor(self, entityid):
     for x in range(self.__width__):
        for y in range(self.__height__):
         list1=self.__grid__[(x,y)]
         if(list1[1]==entityid): 
            return list1[3]
     return None
   def getAgentColor(self, coord):
         list1=self.__grid__[(coord.x,coord.y)]
         if(list1[0]==CellType.EMPTY):
           return None  
         elif list1[0]==CellType.AGENT or list1[0]==CellType.AGENTONDIRT  : 
           return list1[3]
         else:
            return None 
         raise ValueError("Not valid entity ID")  
   def getEntityOrientation(self, coord):
         list1=self.__grid__[(coord.x,coord.y)]
         if(list1[0]==CellType.EMPTY):
           return None  
         elif list1[0]==CellType.AGENT or list1[0]==CellType.USER or list1[0]==CellType.AGENTONDIRT or list1[0]==CellType.USERONDIRT: 
            return list1[2]
         else:
            return None 
         raise ValueError("Not valid coordinate")       
   def getDirtColor(self, coord):
         list1=self.__grid__[(coord.x,coord.y)]
         if(list1[0]==CellType.EMPTY):
           return None  
         elif list1[0]==CellType.DIRT or list1[0]==CellType.AGENTONDIRT or list1[0]==CellType.USERONDIRT: 
            return list1[4]
         else:
            return None 
         raise ValueError("Not valid entity ID")  
       
   def getEntityType(self, entityid):
     for x in range(self.__width__):
        for y in range(self.__height__):
         list1=self.__grid__[(x,y)]
         if(list1[1]==entityid): 
            if(list1[0]== CellType.AGENT or list1[0]== CellType.AGENTONDIRT):
             return CellType.AGENT
            if(list1[0]== CellType.USER or list1[0]== CellType.USERONDIRT):
             return CellType.USER
          
   def getCellTypeOnCoord(self, coord):
        list1=self.__grid__[(coord.x,coord.y)]
        return list1[0]  
        
        raise ValueError("Not valid entity ID")  
   def changeOrientation(self, entityid,orient):
       for x in range(self.__width__):
        for y in range(self.__height__):
         list1=self.__grid__[(x,y)]
         if((list1[1] == entityid)and(not(self.notValidOrientation(orient)))):
          list1[2]=orient
          self.__grid__[(x,y)]=list1
         
      ### NOthing will happen if don't find an entity with this id      


        
   def isVacant(self, coord):  
    if(self.notValidCoordinate(coord)):
       raise ValueError("Invalid Cooridinates")  
    else: 
      list1=self.__grid__[(coord.getX(),coord.getY())] 
      if(list1[0]=="EMPTY"):      
         return True
      else : 
         return False
         
   
   def isOccupied(self,coord):
     if(self.notValidCoordinate(coord)):
        raise ValueError("Invalid coordinate") 
     else:
      list1=self.__grid__[(coord.getX(),coord.getY())]     
      if(list1[0]=="EMPTY"):
       return False
      else: 
       return True
   
   def getFrontCoordinate(self,co,orientation):
    
     if (orientation==Orientation.EAST):
      co2=Coordinate(co.getX(),co.getY()+1)
     elif (orientation==Orientation.WEST):
      co2=Coordinate(co.getX(),co.getY()-1)
     elif (orientation==Orientation.SOUTH):
      co2=Coordinate(co.getX()+1,co.getY())
     else:   #north
      co2=Coordinate(co.getX()-1,co.getY())
     #print(co2) 
     return co2 
   def getLeftCoordinate(self,co,orientation):
    
     if (orientation==Orientation.EAST):
      co2=Coordinate(co.getX()-1,co.getY())
     elif (orientation==Orientation.WEST):
      co2=Coordinate(co.getX()+1,co.getY())
     elif (orientation==Orientation.SOUTH):
      co2=Coordinate(co.getX(),co.getY()+1)
     else:   #north
      co2=Coordinate(co.getX(),co.getY()-1)
     #print(co2) 
     return co2

   def getRightCoordinate(self,co,orientation):
    
     
     if (orientation==Orientation.EAST):
      co2=Coordinate(co.getX()+1,co.getY())
     elif (orientation==Orientation.WEST):
      co2=Coordinate(co.getX()-1,co.getY())
     elif (orientation==Orientation.SOUTH):
      co2=Coordinate(co.getX(),co.getY()-1)
     else:   #north
      co2=Coordinate(co.getX(),co.getY()+1)
     #print(co2) 
     return co2
   def getFrontRightCoordinate(self,co,orientation):
    
     
     if (orientation==Orientation.EAST):
      co2=Coordinate(co.getX()+1,co.getY()+1)
     elif (orientation==Orientation.WEST):
      co2=Coordinate(co.getX()-1,co.getY()-1)
     elif (orientation==Orientation.SOUTH):
      co2=Coordinate(co.getX()+1,co.getY()-1)
     else:   #north
      co2=Coordinate(co.getX()-1,co.getY()+1)
     #print(co2) 
     return co2
 
   def getFrontLeftCoordinate(self,co,orientation):
    
     
     if (orientation==Orientation.EAST):
      co2=Coordinate(co.getX()-1,co.getY()+1)
     elif (orientation==Orientation.WEST):
      co2=Coordinate(co.getX()+1,co.getY()-1)
     elif (orientation==Orientation.SOUTH):
      co2=Coordinate(co.getX()+1,co.getY()+1)
     else:   #north
      co2=Coordinate(co.getX()-1,co.getY()-1)
     #print(co2) 
     return co2
   def makeGUI(self):
    self.printMap()
#    print(self.grid)
  #  print(np.matrix(self.grid))
 #   self.makeGUIFinal()  

   def printMap(self):
     pres = [ [0]*self.__width__ for i in range(self.__height__)]
  
     for i in range(self.__width__):
      for j in range(self.__height__):
          list1=self.__grid__[(i,j)]
          if(list1[0]== "EMPTY"):
             pres[i][j]='_'
          elif(list1[0]== CellType.AGENT or list1[0]==CellType.USER): 
             if(list1[2]==Orientation.SOUTH):          
                pres[i][j]='v'
             elif(list1[2]==Orientation.NORTH):          
                pres[i][j]='^'
             elif(list1[2]==Orientation.EAST):          
                pres[i][j]='>'
             elif(list1[2]==Orientation.WEST):          
                pres[i][j]='<'
             else:
                pres[i][j]='o'
         
          elif(list1[0]== CellType.DIRT): 
             pres[i][j]='~'
          elif(list1[0]== CellType.AGENTONDIRT or list1[0]== CellType.USERONDIRT): 
             if(list1[2]==Orientation.SOUTH):          
                pres[i][j]='~v'
             elif(list1[2]==Orientation.NORTH):          
                pres[i][j]='~^'
             elif(list1[2]==Orientation.EAST):          
                pres[i][j]='~>'
             elif(list1[2]==Orientation.WEST):          
                pres[i][j]='~<'
             else:
                pres[i][j]='o'
              
     print(np.matrix(pres))

  
   def makeGUIFinal(self):
    self. window = Tk()
    self.window.geometry("300x300+500+400") # size of the window width:- 500, height:- 375
    self.window.resizable(0, 0) # this prevents from resizing the window
    self.window.title("Grid World")
   # self.window.after(1000, lambda: self.window.destroy())    
   

    self.btns_frame = Frame(self.window, width = 300, height = 300, bg = "grey")
  
    
    blank= '../img/empty.jpg'
    East= '../img/robot_e.jpg'
    West= '../img/robot_w.jpg'
    South= '../img/robot_s.jpg'
    North= '../img/robot_n.jpg'
    
   
    
    Error='../img/error.png'
    
    
    im = Image.open(blank)
    self.empty = ImageTk.PhotoImage(im)
    im2 = Image.open(North)
    self.north = ImageTk.PhotoImage(im2)
    
    im3 = Image.open(East)
    self.east = ImageTk.PhotoImage(im3)
    
    im4 = Image.open(West)
    self.west = ImageTk.PhotoImage(im4) 
    im5 = Image.open(South)
    self.south = ImageTk.PhotoImage(im5)
    
  
    
    
    im10 = Image.open(Error)
    self.errorimage = ImageTk.PhotoImage(im10)
    
    
    
    
    
    
    
    i=0  
    while(i < self.height):
     j=0   
     while(j < self.width):
      
       list1=self.grid[(i,j)]
       if(list1[0]== "EMPTY"):
              bt=Button(self.btns_frame,image=self.empty, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
       elif(list1[0]== CellType.AGENT): 
             if(list1[3]==Orientation.SOUTH):          
                bt = Button(self.btns_frame, image=self.south, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
             elif(list1[3]==Orientation.NORTH):          
                bt = Button(self.btns_frame, image=self.north, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
             elif(list1[3]==Orientation.EAST):          
                bt = Button(self.btns_frame, image=self.east, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
             elif(list1[3]==Orientation.WEST):          
                bt = Button(self.btns_frame, image=self.west, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
       elif(list1[0]== CellType.DIRT): 
                bt = Button(self.btns_frame, image=self.errorimage, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
       elif(list1[0]== CellType.AGENTONDIRT): 
             if(list1[6]==Orientation.SOUTH):          
                bt = Button(self.btns_frame, image=self.north, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
             elif(list1[6]==Orientation.NORTH):          
                bt = Button(self.btns_frame, image=self.north, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)         
             elif(list1[6]==Orientation.EAST):          
                bt = Button(self.btns_frame, image=self.north, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)          
             elif(list1[6]==Orientation.WEST):          
                bt = Button(self.btns_frame, image=self.north, fg = "black", width = 50, height = 50, bd = 0, bg = "#fff", cursor = "hand2").grid(row = i, column = j, padx = 1, pady = 1)
    
       j=j+1
     i=i+1   
    self.btns_frame.pack()
    self.window.mainloop()
    

    
       
#p= PhysicalAllocationMap(5,5)   

#p.placeEntity(Coordinate(1,0),3,CellType.AGENT,AgentColor.GREEN,Orientation.EAST)
#p.placeEntity(Coordinate(3,0),2,CellType.DIRT,DirtColor.GREEN,Orientation.ALL)

#p.placeEntity(Coordinate(2,0),2,CellType.DIRT,DirtColor.GREEN,Orientation.ALL)
#p.placeEntity(Coordinate(2,0),2,CellType.AGENT,DirtColor.GREEN,Orientation.EAST)#

#p.makeGUI()


