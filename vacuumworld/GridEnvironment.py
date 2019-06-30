from pystarworlds.Environment import Ambient,Physics, Environment
from pystarworlds.Factories import PerceptionFactory,RuleFactory
from VWFactories import VWGridPerceptionFactory,ForwardActionRuleFactory,TurnLeftActionRuleFactory,TurnRightActionRuleFactory,CleanActionRuleFactory,DropActionRuleFactory,SpeakActionRuleFactory,SpeakToAllActionRuleFactory,ForwardActionExecuteFactory,TurnLeftActionExecuteFactory,TurnRightActionExecuteFactory,CleanActionExecuteFactory,DropActionExecuteFactory,SpeakActionExecuteFactory,SpeakToAllActionExecuteFactory
from GridPerception import Observation,Message,ActionResultPerception
from EntityType import AgentColor,DirtColor,ActorType
from ActionType import ActionResult,ActionType
from GridWorldAction import ForwardMoveMentAction,MoveLeftAction,MoveRightAction, CleanDirtAction,DropDirtAction, SpeakAction,BroadcastAction
#from vw import Direction

class GridAmbient(Ambient):
    def __init__(self, agents,objects, allocationMap ):
        super().__init__(agents,objects)
        self.__allocationMap__=allocationMap
        
    def getPlacementMap(self):
        return self.__allocationMap__
    

class GridPhysics(Physics):
 pass   
    
              
               
   
    
class GridEnvironment(Environment):
     
     def setupFactories(self):

      self.perception_factories = [VWGridPerceptionFactory()]
      self.rule_factories = [ForwardActionRuleFactory(),TurnLeftActionRuleFactory(),TurnRightActionRuleFactory(),CleanActionRuleFactory(),DropActionRuleFactory(),SpeakActionRuleFactory(),SpeakToAllActionRuleFactory()]
      self.executeaction_factories = [ForwardActionExecuteFactory(),TurnLeftActionExecuteFactory(),TurnRightActionExecuteFactory(),CleanActionExecuteFactory(),DropActionExecuteFactory(),SpeakActionExecuteFactory(),SpeakToAllActionExecuteFactory()]
 
    
     def simulate(self, cycles):
        self.getAmbient().getPlacementMap().makeGUI()
        self.setupFactories()
        i=0
        while(i<cycles):
          print("_______________________________________________________________________________")
          print("_______________________________________________________________________________")
          print("  Time stamp ")
          print(i)
          self.evolveEnvironment()   
          i=i+1
          self.getAmbient().getPlacementMap().makeGUI()
          
 







 
#####################################################################################################################   
     def sendFailedAttemptsResponse(self,action, result):
      per=ActionResultPerception(action.getActor(),type(action), result)
     

      sensors = self.getPhysics().EventSensorsDirectory[type(per)] # get type of all sensors to be notified
      for s in sensors:
          if(s.getOwner()==(per.getOwner())):
             s.notifyEvent(per)    
             
###################################################################################################################             
             
             
             
############################################################    Factories              #


             
