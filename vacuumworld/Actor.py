from GenericAgent.Agent import Mind



from BasicBuildingBlock.Coordinate import Coordinate
from GridWorld.Orientation_Direction import Orientation
from GridWorld.GridPerception import VWGridVisionPerception,VWCommunicationPerception
from GridWorldAction import  ChangeOrientationAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,CleanAction,DropAction
from GenericAgent.Agent import AgentBody 
from GridWorld.EntityType import ActorType
class UserBody(AgentBody):
    
    def __init__(self, mind, actuators, sensors,orientation):
        super().__init__(mind,actuators,sensors)
        self.__orientation__=orientation
        self.__actorType__=ActorType.USER
    def getOrientation(self):
        return self.__orientation__
    def getActorType(self):
        return self.__actorType__
         
        

class UserMind(Mind):
       
   def __post_init__(self, body):
        super().__post_init__(body)
        self.team=[]
      
  
    #@abstractmethod
   
   def perceive(self):
    super().perceive()
    
    
   def decide(self):  # deliberate
       ag=super().getAgent()
 
      
       agentID=ag.getID()
       perceptions=[]
       perceptions=super().getPerceptions()
       actions=[]
       
       Desiredact=NoMoveMentAction()
       if(len(perceptions)==0):
          print("zero perception")
          print(" user")
         
          actions.append(NoMoveMentAction())
       else:
        ### sort perceptions process visionones first and then communication   
        for per in perceptions:
          Desiredact=None     
          if(type(per)==VWGridVisionPerception):
              if(not(per.iamSittingOnDirt())):
                Desiredact=DropAction(agentID,per.getCoordinates())
              elif per.canMoveForward():
                Desiredact=ForwardMoveMentAction(agentID,per.getCoordinates(),per.getCoordinatesForward())
              else:    
               if(per.getOrientation()==Orientation.SOUTH):
                changeOrient=Orientation.WEST
               elif(per.getOrientation()==Orientation.EAST):
                changeOrient=Orientation.SOUTH
               elif(per.getOrientation()==Orientation.NORTH):
                changeOrient=Orientation.EAST
               else:
                changeOrient=Orientation.NORTH
               Desiredact=ChangeOrientationAction(agentID,changeOrient)
              actions.append(Desiredact)
              for action in actions:
               for ac in ag.getActuators():
                if(ac.isCompatible(Desiredact)):
                  ac.attempt(Desiredact)
            
          
   

# -*- coding: utf-8 -*-

