from . import vwaction as action
from . import vwuser
from . import vwagent
from . import vwc

from pystarworlds.Environment import Ambient, Physics, Environment, Process
from pystarworlds.Identifiable import Identifiable

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
            if entity:
                if entity.agent:       
                    if entity.agent.colour != vwc.colour.user:
                        ag = vwagent.CleaningAgentBody(entity.agent.name,
                                                       copy.deepcopy(minds[entity.agent.colour]),
                                                       entity.agent.orientation,
                                                       entity.coordinate,
                                                       entity.agent.colour)
                        agents.append(ag)
                    else:                        
                        ag = vwuser.UserBody(entity.agent.name, 
                                             vwuser.UserMind(),
                                             entity.agent.orientation,
                                             entity.coordinate,
                                             entity.agent.colour)
                        agents.append(ag)
                elif(entity.dirt):       
                    dirts.append(Dirt(entity.dirt))
        super(GridAmbient, self).__init__(agents, dirts)


class GridPhysics(Physics):
    pass

class GridEnvironment(Environment):
    
    def __init__(self, ambient):
        
        actions = [action.DropAction, action.MoveAction,
                   action.TurnAction, action.CleanAction, 
                   action.CommunicativeAction]
        
        physics = GridPhysics(actions)
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()], actions)

class Dirt(Identifiable):
    
    def __init__(self, dirt):
        self.ID = dirt.name
        super(Dirt, self).__init__()
        self.dirt = dirt

class ObservationProcess(Process):
    
    def __call__(self, env):
        for agent in env.ambient.agents.values():
            env.physics.notify_agent(agent, self.__get_perception__(env.ambient, agent))
            
    def __get_perception__(self, ambient, agent):
        c = agent.coordinate
        f = vwc.orientation_map[agent.orientation]
        l = vwc.orientation_map[vwc.left(agent.orientation)]
        r = vwc.orientation_map[vwc.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = vwc.observation(ambient.grid.state[c], 
                        ambient.grid.state[c + l],
                        ambient.grid.state[c + r], 
                        ambient.grid.state[c + f], 
                        ambient.grid.state[c + f + l],
                        ambient.grid.state[c + f + r])            
        return obs


