from . import vwaction as action
from . import vwagent
from . import vwc
from . import vwuser

from pystarworlds.Environment import Ambient, Physics, Environment, Process
from pystarworlds.Identifiable import Identifiable

import copy


#from VWFactories import VWGridPerceptionFactory,ForwardActionRuleFactory,TurnLeftActionRuleFactory,TurnRightActionRuleFactory,CleanActionRuleFactory,DropActionRuleFactory,SpeakActionRuleFactory,SpeakToAllActionRuleFactory,ForwardActionExecuteFactory,TurnLeftActionExecuteFactory,TurnRightActionExecuteFactory,CleanActionExecuteFactory,DropActionExecuteFactory,SpeakActionExecuteFactory,SpeakToAllActionExecuteFactory
#from GridPerception import Observation,Message,ActionResultPerception
#from GridWorldAction import ForwardMoveMentAction,MoveLeftAction,MoveRightAction, CleanDirtAction,DropDirtAction, SpeakAction,BroadcastAction
#from vw import Direction
#from pystarworlds.Identifiable import Identifiable

def init(grid, minds, user_mind):
    minds[vwc.colour.user] = vwuser.USERS[user_mind]()
    return GridEnvironment(GridAmbient(grid, minds))
    
class GridAmbient(Ambient):
    
    def __init__(self, grid, minds):
        self.grid = grid
        self.mind_types = set(type(mind) for mind in minds)
        agents = []
        dirts = []
        for location in grid.state.values(): 
            if location:
                if location.agent:       
                    agents.append(self.init_agent(location, self.get_type(location), minds))
                if location.dirt:       
                    dirts.append(Dirt(location.dirt))
        super(GridAmbient, self).__init__(agents, dirts)
    
    def get_type(self, location):
        return vwagent.agent_type[int(location.agent.colour == vwc.colour.user)]
        
    def init_agent(self, location, _type, minds):
        return vwagent.VWBody(_type, location.agent.name, copy.deepcopy(minds[location.agent.colour]),
                              location.agent.orientation, location.coordinate, location.agent.colour)
        

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
            env.physics.notify_agent(agent, self.get_perception(env.ambient.grid, agent))
            
    def get_perception(self, grid, agent):
        c = agent.coordinate
        f = vwc.orientation_map[agent.orientation]
        l = vwc.orientation_map[vwc.left(agent.orientation)]
        r = vwc.orientation_map[vwc.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = vwc.observation(grid.state[c], 
                        grid.state[c + l],
                        grid.state[c + r], 
                        grid.state[c + f], 
                        grid.state[c + f + l],
                        grid.state[c + f + r])            
        return obs


