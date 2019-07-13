
from . import vwsensor as sense
from . import vwactuator as act
from . import vwaction as action
from . import vwuser
from . import vwagent
from . import vwfactories as factory

from .vwc import colour, observation, message


from pystarworlds.Environment import Ambient,Physics, Environment



#from VWFactories import VWGridPerceptionFactory,ForwardActionRuleFactory,TurnLeftActionRuleFactory,TurnRightActionRuleFactory,CleanActionRuleFactory,DropActionRuleFactory,SpeakActionRuleFactory,SpeakToAllActionRuleFactory,ForwardActionExecuteFactory,TurnLeftActionExecuteFactory,TurnRightActionExecuteFactory,CleanActionExecuteFactory,DropActionExecuteFactory,SpeakActionExecuteFactory,SpeakToAllActionExecuteFactory
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import ForwardMoveMentAction,MoveLeftAction,MoveRightAction, CleanDirtAction,DropDirtAction, SpeakAction,BroadcastAction
#from vw import Direction
#from pystarworlds.Identifiable import Identifiable

def init(grid):
    return GridEnvironment(GridAmbient(grid))
    
class GridAmbient(Ambient):
    
    def __init__(self, grid):
        self.grid = grid
        agents=[]
        dirts=[]
        for entity in grid.state.values():       
            if entity.agent:       
                if entity.agent.colour != colour.user:
                    ag = vwagent.CleaningAgentBody(vwagent.CleaningAgentMind(),
                              [act.MovementActuator(), act.CommunicationActuator(), act.CleaningDirtActuator()],
                              [sense.VisionSensor(), sense.CommunicationSensor()],
                              entity.agent.direction,
                              entity.coordinate,
                              entity.agent.colour)
                    agents.append(ag)
                else:                        
                    ag = vwuser.UserBody(vwuser.UserMind(),
                               [act.MovementActuator(), act.DropDirtActuator()],
                               [sense.VisionSensor(), sense.CommunicationSensor()],
                               entity.agent.direction,
                               entity.coordinate,
                               entity.agent.colour)
                    agents.append(ag)
            elif(entity.dirt):       
                dirts.append(entity.dirt)
        super(GridAmbient, self).__init__(agents, dirts)


class GridPhysics(Physics):
    pass

class GridEnvironment(Environment):
    
    def __init__(self, ambient):
        
        actions = [action.DropDirtAction, action.ForwardMoveMentAction, action.MoveRightAction,
                   action.MoveLeftAction, action.CleanDirtAction, action.SpeakAction, action.BroadcastAction]
        
        physics = GridPhysics({sense.VisionSensor:[observation], 
                               sense.CommunicationSensor:[message]})
        
        super(GridEnvironment, self).__init__(physics, ambient, actions,
             [s for a in ambient.agents.values() for s in a.sensors]) #Nausheen use this in Environment
        
        self.perception_factories = [factory.VWObservationFactory()]
        
        #make this a dictionary type(action) -> rule
        self.rule_factories = [factory.ForwardActionRuleFactory(),
                               factory.TurnLeftActionRuleFactory(),
                               factory.TurnRightActionRuleFactory(),
                               factory.CleanActionRuleFactory(),
                               factory.DropActionRuleFactory(),
                               factory.SpeakActionRuleFactory(),
                               factory.SpeakToAllActionRuleFactory()]
        
        #make this a dictionary type(action) -> rule
        self.executeaction_factories = [factory.ForwardActionExecuteFactory(),
                                        factory.TurnLeftActionExecuteFactory(),
                                        factory.TurnRightActionExecuteFactory(),
                                        factory.CleanActionExecuteFactory(),
                                        factory.DropActionExecuteFactory(),
                                        factory.SpeakActionExecuteFactory(),
                                        factory.SpeakToAllActionExecuteFactory()]
          
#####################################################################################################################
'''
   def sendFailedAttemptsResponse(self,action, result):
      per=ActionResultPerception(action.getActor(),type(action), result)


      sensors = self.getPhysics().EventSensorsDirectory[type(per)] # get type of all sensors to be notified
      for s in sensors:
          if(s.getOwner()==(per.getOwner())):
             s.notifyEvent(per)
'''
###################################################################################################################



############################################################    Factories              #



