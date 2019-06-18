from GenericAgent.Agent import Mind



from BasicBuildingBlock.Coordinate import Coordinate
from GridWorld.Orientation_Direction import Orientation
from GridWorld.GridPerception import VWGridVisionPerception,VWCommunicationPerception,VWActionResultPerception
from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,BroadcastAction,NoMoveMentAction,CleanAction,DropAction
from GenericAgent.Agent import AgentBody 
from GridWorld.EntityType import ActorType
class CleaningAgentBody(AgentBody):
    
    def __init__(self, mind, actuators, sensors,orientation,color):
        super().__init__(mind,actuators,sensors)
        self.__orientation__=orientation
        self.__color__=color
        self.__actorType__=ActorType.AGENT
    def getOrientation(self):
        return self.__orientation__
    def getActorType(self):
        return self.__actorType__
         
     
    def getColor(self):
        return self.__color__
        

class CleaningAgentMind(Mind):
       
   def __post_init__(self, body):
        super().__post_init__(body)
        self.team=[]
      
  
    #@abstractmethod
   def revise(self):
    pass
       
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
          print("--zero perception--")
          print(agentID)
          actions.append(NoMoveMentAction())
       else:
        ### sort perceptions process visionones first and then communication   
        for per in perceptions:
           Desiredact=None     
           if(type(per)==VWGridVisionPerception):
               
               if(per.amICleaningAgent() and per.amISittingOnDirt()):  
                    Desiredact=CleanAction(agentID,per.getCoordinates())
                    actions.append(Desiredact)
                                     
               elif(per.amICleaningAgent() and ((per.canMoveForward())==False) ):
                    
                    Desiredact=MoveRightAction(agentID,per.getOrientation())
                    actions.append(Desiredact)
               elif (per.amICleaningAgent() and per.canMoveForward()):             
                     Desiredact=ForwardMoveMentAction(agentID,per.getCoordinates(),per.getCoordinatesForward())
                     actions.append(Desiredact)
              
           elif(type(per)==VWCommunicationPerception):
              print(per.getSender())  
              print(per.getMessage())  
           elif(type(per)==VWActionResultPerception):
              print(per.getResult())

        for action in actions:
                  for ac in ag.getActuators():
                    if(ac.isCompatible(Desiredact)):
                      ac.attempt(Desiredact)
