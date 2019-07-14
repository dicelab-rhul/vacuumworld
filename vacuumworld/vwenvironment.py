
from . import vwsensor as sense
from . import vwactuator as act
from . import vwaction as action
from . import vwuser
from . import vwagent
from . import vwfactories as factory

from .vwc import colour, observation, message


from pystarworlds.Environment import Ambient, Physics, Environment
from pystarworlds.Event import Event
import copy


#from VWFactories import VWGridPerceptionFactory,ForwardActionRuleFactory,TurnLeftActionRuleFactory,TurnRightActionRuleFactory,CleanActionRuleFactory,DropActionRuleFactory,SpeakActionRuleFactory,SpeakToAllActionRuleFactory,ForwardActionExecuteFactory,TurnLeftActionExecuteFactory,TurnRightActionExecuteFactory,CleanActionExecuteFactory,DropActionExecuteFactory,SpeakActionExecuteFactory,SpeakToAllActionExecuteFactory
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import ForwardMoveMentAction,MoveLeftAction,MoveRightAction, CleanDirtAction,DropDirtAction, SpeakAction,BroadcastAction
#from vw import Direction
#from pystarworlds.Identifiable import Identifiable

def init(grid, minds):
    return GridEnvironment(GridAmbient(grid, minds))
    
class GridAmbient(Ambient):
    
    def __init__(self, grid, minds):
        self.grid = grid
        agents=[]
        dirts=[]
        for entity in grid.state.values():       
            if entity.agent:       
                if entity.agent.colour != colour.user:
                    ag = vwagent.CleaningAgentBody(copy.deepcopy(minds[entity.agent.colour]),
                                                   entity.agent.orientation,
                                                   entity.coordinate,
                                                   entity.agent.colour)
                    agents.append(ag)
                else:                        
                    ag = vwuser.UserBody(vwuser.UserMind(),
                               [act.UserActuator(), act.CommunicationActuator()],
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
        
        actions = [action.DropAction, action.MoveAction,
                   action.TurnAction, action.CleanAction, 
                   action.CommunicativeAction]
        
        physics = GridPhysics({sense.VisionSensor:[observation], 
                               sense.CommunicationSensor:[message]})
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()], actions,
             [s for a in ambient.agents.values() for s in a.sensors()]) #Nausheen use this in Environment
        
        self.perception_factories = [factory.ObservationFactory()]
        
        '''
        rules = [factory.ForwardActionRuleFactory(),
                   factory.TurnLeftActionRuleFactory(),
                   factory.TurnRightActionRuleFactory(),
                   factory.CleanActionRuleFactory(),
                   factory.DropActionRuleFactory(),
                   factory.SpeakActionRuleFactory(),
                   factory.SpeakToAllActionRuleFactory()]
        

        #rename this to rules
        self.rule_factories = {r._type:r for r in rules}

        executors = [factory.ForwardActionExecuteFactory(),
                        factory.TurnLeftActionExecuteFactory(),
                        factory.TurnRightActionExecuteFactory(),
                        factory.CleanActionExecuteFactory(),
                        factory.DropActionExecuteFactory(),
                        factory.SpeakActionExecuteFactory(),
                        factory.SpeakToAllActionExecuteFactory()]
  
        self.executeaction_factories = {e._type:e for e in executors}
        '''

class ObservationProcess:
    
    def __init__(self):
        self. obs_factory = factory.ObservationFactory()
    
    def __call__(self, env):
        for agent in env.ambient.agents.values():
            print("observation for agent", agent)
            env.physics.notify_agent(agent, self.obs_factory(env.ambient, agent))


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



