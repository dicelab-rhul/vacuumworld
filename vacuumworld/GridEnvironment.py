from GenericEnvironment.Environment import Ambient,Physics, Environment
from GridWorld.GridPerception import VWGridVisionPerception,VWCommunicationPerception,VWActionResultPerception
from GridWorld.EntityType import AgentColor,DirtColor,ActorType
from GridWorld.ActionType import ActionResult,ActionType
from GridWorldAction import ForwardMoveMentAction,MoveLeftAction,MoveRightAction, CleanAction,DropAction, SpeakAction,BroadcastAction

class GridAmbient(Ambient):
    def __init__(self, agents,objects, allocationMap ):
        super().__init__(agents,objects)
        self.__allocationMap__=allocationMap
        
    def getPlacementMap(self):
        return self.__allocationMap__
    
   
    
    def __unicode__(self):
        return self.__str__()
    def __repr__(self):
        return self.__str__()

class GridPhysics(Physics):
    
     def isCompatible(self, actorColor,dirtColor):
       if(actorColor==AgentColor.WHITE and (dirtColor==DirtColor.GREEN or dirtColor==DirtColor.ORANGE)):
         return True
       elif(actorColor==AgentColor.GREEN and dirtColor==DirtColor.GREEN):
         return True
       elif(actorColor==AgentColor.ORANGE and dirtColor==DirtColor.ORANGE):
         return True
       else:
         return False
     
     def isPossible(self, action,ambient,actionList):
      flag=True 
      if(actionList.count(type(action)==0)):       # if action in not in action list undefined action 
       flag=False
      if((type(action)==ForwardMoveMentAction)):    # if forward 
       if(ambient.getPlacementMap().notValidCoordinate(action.getnewCoordinate())): 
        flag=False
       elif(ambient.getPlacementMap().isOccupiedByActor(action.getnewCoordinate())): 
        flag=False
        
      
      elif(type(action)==MoveRightAction or type(action)==MoveLeftAction ):
       if(ambient.getPlacementMap().notValidOrientation(action.getOrient())):
           flag=False
      
      elif(type(action)==CleanAction):
       if(ambient.getPlacementMap().getEntityType(action.getActor())==ActorType.USER): 
        flag=False  
       if(not(self.isCompatible(ambient.getPlacementMap().getAgentColor(action.getCoordinate()),ambient.getPlacementMap().getDirtColor(action.getCoordinate())))): 
        flag=False
       
      elif(type(action)==DropAction):
        pass
      elif(type(action)==SpeakAction):
         pass        
      return flag
    
     def verifyAttempts(self,attempts,ambient,valid_actions):
         validityvalues=[]
         for at in attempts:
            validityvalues.append(ActionResult.SUCCESS)
          
         i=0
         while(i<len(attempts)):
          j=i+1
          action=attempts[i]
            
          while(j<len(attempts)):
            act=attempts[j]
            if((act.isSame(action))and(validityvalues[j]==ActionResult.SUCCESS)): 
                validityvalues[j]=ActionResult.FAILURE
                    
            if((self.isPossible(act,ambient,valid_actions)==False)):
                 validityvalues[j]=ActionResult.IMPOSSIBLE
            if((self.isPossible(action,ambient,valid_actions)==False)):
                validityvalues[i]=ActionResult.IMPOSSIBLE
            j=j+1
          i=i+1
           
         return validityvalues  
           
    

class VWGridPerceptionFactory:
    
    def __init__(self):
        super(self, VWGridPerceptionFactory).__init__(type(VWGridVisionPerception))
    
    def __call__(self, env, agent, sensor):
        return VWGridVisionPerception(agent.getID(), env.getAmbient().getPlacementMap())
          
    
class GridEnvironment(Environment):
    
    
    #this should be general ( a general notification mechanism for sensors)
   def notifyCommunicationPerception(self,per):   
          sensors = self.getPhysics().EventSensorsDirectory[type(per)] # get type of all sensors to be notified
          for s in sensors:
           if(s.getOwner()==(per.getOwner())):
             s.notifyEvent(per)
       
        
   def simulate(self, cycles):
        self.getAmbient().getPlacementMap().makeGUI()
        i=0
        perception_factories = [VWGridPerceptionFactory()]
        while(i<cycles):
    
        #for i in range(cycles) and self.end==False:
          print("_______________________________________________________________________________")
          print("_______________________________________________________________________________")
          print("  Time stamp ")
          print(i)
          
 
        #  print("\n--- " + str(self) + " t=" + str(i) 
          self.evolveEnvironment(perception_factories)   
          i=i+1
          self.getAmbient().getPlacementMap().makeGUI()
          
 
   #this should be general (use factories)
   def executeActions(self,attempts,validityvalues):      
            print(attempts) 
            k=0
            for action in attempts:
              if(validityvalues[k]==ActionResult.SUCCESS):
                if(type(action)==BroadcastAction):
                  for ag in self.getAmbient().getAgents():  
                    per=VWCommunicationPerception(action.geSender(),ag.getID(),action.getMessage())
                    self.notifyCommunicationPerception(per)
                elif (type(action)==SpeakAction):
                  per=VWCommunicationPerception(action.geSender(),action.getReceiver(),action.getMessage())
                  self.notifyCommunicationPerception(per)
                else:
                 action.execute(self.getAmbient().getPlacementMap())  
              k=k+1     
            k=0
            for action in attempts:
              if(validityvalues[k]==ActionResult.IMPOSSIBLE or validityvalues[k]==ActionResult.FAILURE):
                  self.getPhysics().sendFailedAttemptsResponse(action,validityvalues[k])    
              
              k=k+1     
          
   def sendFailedAttemptsResponse(self,action, result):
      if((type(action)==ForwardMoveMentAction)):    # if forward 
         per=VWActionResultPerception(action.getActor(),ActionType.MOVEFORWARD, result)
      elif(type(action)==MoveRightAction):    # if forward 
         per=VWActionResultPerception(action.getActor(),ActionType.MOVERIGHT,result)
      elif(type(action)==MoveLeftAction):    # if forward 
         per=VWActionResultPerception(action.getActor(),ActionType.MOVELEFT, result)
      elif(type(action)==CleanAction):    # if forward 
         per=VWActionResultPerception(action.getActor(),ActionType.CLEANDIRT, result)
      elif(type(action)==DropAction):    # if forward 
         per=VWActionResultPerception(action.getActor(),ActionType.DROPDIRT, result)
      
         

      sensors = self.getPhysics().EventSensorsDirectory[type(per)] # get type of all sensors to be notified
      for s in sensors:
          if(s.getOwner()==(per.getOwner())):
             s.notifyEvent(per)    