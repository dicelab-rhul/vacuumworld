from pystarworlds.Agent import Mind



from GridPerception import Observation,Message
from GridWorldAction import  MoveRightAction,MoveLeftAction,ChangeOrientationAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,CleanDirtAction,DropDirtAction
from pystarworlds.Agent import AgentBody 
from pystarworlds.Factories import ActionFactory 
from VWFactories import Speak,SpeakToAll,Move,TurnLeft,TurnRight,DropDirt
from vwc import coord,colour,location,action,observation,perception,message

import random
class UserBody(AgentBody):
    
    def __init__(self,name, mind, actuators, sensors,orientation,coordiante,color):
        super().__init__(name,mind,actuators,sensors)
        self.__orientation__=orientation
        self.__color__=color
        self.__coordiante__=coordiante
        
    def getOrientation(self):
        return self.__orientation__
    def getCoordinate(self):
        return self.__coordinate__
  
       # return self.color
    def setOrientation(self,orient):
        self.__orientation__=orient
    def setCoordinate(self,coor):
        self.__coordinate__=coor
     
    def getID(self):
        return super().getName()      
        

class UserMind(Mind):
       
   def __post_init__(self, body):
        super().__post_init__(body)
        self.percept=None  
  
    #@abstractmethod
   
   def perceive(self):
    super().perceive()
    perceptions=super()._getPerceptions()
  
    
    obser=None
    for per in perceptions:
      if(type(per)==Observation):
         obser=per.observation
     
    #      messages.append(mess)
     
        
 
    self.percept=perception(obser,None)
    self.getBody().setCoordinate(self.percept.observation.center.coordinate)
    self.getBody().setOrientation(self.percept.observation.center.agent.direction)
    
   def decide(self):  # deliberate
            
    
       if(self.percept==None):
          print("--zero perception--")
         
       else:
        ### sort perceptions process visionones first and then communication   
        
        if self.percept.observation==None:
            print("No visual perception")
        
        
               
                   
        if(self.percept.observation.center.agent and self.percept.observation.forward==None) or(self.percept.observation.center.agent and self.percept.observation.forward.agent!=None):  # wall or agent in front 
                   
                   print("change orientation")
                   act=TurnLeft(self)
                  
                       
              
        elif (self.percept.observation.center.agent and self.percept.observation.center.dirt==None):
                   print("Drop Dirt")
                   r=random.randint(1,3)
                   act=DropDirt(self) 
                
  
        elif self.percept.observation.center.agent!=None and self.percept.observation.center.dirt!=None:
                     print("move forward")
                     act=Move(self)
      
                 
         
        

