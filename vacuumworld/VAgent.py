from pystarworlds.Agent import Mind




from GridPerception import Observation,Message,ActionResultPerception
from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction
from pystarworlds.Agent import AgentBody
from pystarworlds.Factories import ActionFactory 
from VWFactories import Speak,SpeakToAll,Move,TurnLeft,TurnRight,CleanDirt

from vwc import coord,colour,location,action,observation,perception,message
from collections import namedtuple



class CleaningAgentBody(AgentBody):
    
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
     
    def getColor(self):
        return self.__color__
        

class CleaningAgentMind(Mind):
       
   def __post_init__(self, body):
        super().__post_init__(body)
        
        self.percept=None  
#       
           
    #@abstractmethod
  
    
   def revise(self):
    pass
       
   def perceive(self):
    super().perceive()
    perceptions=super()._getPerceptions()
    messages=None#[]
    obser=None
    messages = []
    for per in perceptions:
      if(type(per)==Observation):
         obser=per.observation
      elif(type(per)==Message):
          messages.append(message(per.getSender(),per.getMessage()))
    #      messages.append(mess)
    self.percept=perception(obser,messages)
    self.getBody().setCoordinate(self.percept.observation.center.coordinate)
    self.getBody().setOrientation(self.percept.observation.center.agent.direction)

    
    def do(self):
#        if ...
 #           return actions.move
       pass  
        
    
    
    
   def decide(self):  # deliberate
    #   mind.do()
       
       
   #    mind.speak()
       


    
       if(self.percept==None):
          print("--zero perception--")
         
       else:
        ### sort perceptions process visionones first and then communication   
        
        if self.percept.observation==None:
            print("No visual perception")
        
        
        elif self.percept.observation.center.agent!=None and self.percept.observation.center.dirt!=None:
         #  print(self.percept.observation.center.agent)
          # print(self.percept.observation.center.dirt)
           if((self.percept.observation.center.agent.colour=="green"  or  self.percept.observation.center.agent.colour=="white")and(self.percept.observation.center.dirt.colour=="green")):
                     print("clean")
                     act=CleanDirt(self)
           elif((self.percept.observation.center.agent.colour=="orange"  or  self.percept.observation.center.agent.colour=="white")and(self.percept.observation.center.dirt.colour=="orange")):
                     print("clean")
                     act=CleanDirt(self)
             
           else:
                   print("move forward")
                   act=Move(self)
                
                   
        elif(self.percept.observation.center.agent and self.percept.observation.forward==None) or(self.percept.observation.center.agent and self.percept.observation.forward.agent!=None):  # wall or agent in front 
                   print("change orientation")
                   act=TurnLeft(self)
                   if(self.percept.observation.forward!=None):
                     if(self.percept.observation.forward.agent!=None):
                        act=Speak(self,self.percept.observation.forward.agent.name,"Excuse me you are blocking me")
                       
              
        elif (self.percept.observation.center.agent and self.percept.observation.forward!=None and self.percept.observation.forward.agent==None):
                   print("move forward and broadcast ")
                   act=Move(self)
                   act=SpeakToAll(self,"AAAOAAA")
                   

  
        
        if self.percept.messages==None:
            print("No message perception")
                
        else:
            for message in self.percept.messages:
             print(message.sender)
             print(message.content)
          
        


    



