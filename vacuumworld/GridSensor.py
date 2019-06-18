from BasicBuildingBlock.Sensor import Sensor

class VisionSensor(Sensor):

  def __init__(self):
    super().__init__()

  def notifyEvent(self,event):
   super().notifyEvent(event)


  def getPercepion(self):
   return super().getPercepion()

  def isEmpty(self):
   return  super().isEmpty()    
     
class CommunicationSensor(Sensor):  # ear for getting a communication perception
   def __init__(self):
    super().__init__()
  
   
   def notifyEvent(self,event):
    super().notifyEvent(event)

   def getPercepion(self):
    return super().getPercepion()

    
   def isEmpty(self):
    return  super().isEmpty()    

       # -*- coding: utf-8 -*-

