
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

from . import vwfactories

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
            if entity:
                if entity.agent:       
                    if entity.agent.colour != colour.user:
                        ag = vwagent.CleaningAgentBody(copy.deepcopy(minds[entity.agent.colour]),
                                                       entity.agent.orientation,
                                                       entity.coordinate,
                                                       entity.agent.colour)
                        ag.ID = entity.agent.name
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
        
        executors = [vwfactories.CommunicationExecutor(), 
                     vwfactories.DropExecutor(), 
                     vwfactories.CleanExecutor(), 
                     vwfactories.TurnExecutor(), 
                     vwfactories.MoveExecutor()]
        preconditions = [vwfactories.MovePrecondition(),
                         vwfactories.CleanPrecondition(),
                         vwfactories.DropPrecondition()]
        
        
        physics = GridPhysics({sense.VisionSensor:[observation], 
                               sense.CommunicationSensor:[message]},
                               preconditions,
                               executors)
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()], actions)
        
        self.perception_factories = [factory.ObservationFactory()]

class ObservationProcess:
    
    def __init__(self):
        self. obs_factory = factory.ObservationFactory()
    
    def __call__(self, env):
        for agent in env.ambient.agents.values():
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



