from . import vwaction as action
from . import vwagent
from . import vwc
from . import vwuser

from pystarworlds.Environment import Ambient, Physics, Environment, Process
from pystarworlds.Identifiable import Identifiable

import copy



def init(grid, minds, user_mind):
    minds[vwc.Colour.user] = vwuser.USERS[user_mind]()
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
                    agents.append(GridAmbient.init_agent(location, GridAmbient.get_type(location), minds))
                if location.dirt:       
                    dirts.append(Dirt(location.dirt))
        super(GridAmbient, self).__init__(agents, dirts)
    
    @staticmethod
    def get_type(location):
        return vwagent.agent_type[int(location.agent.colour == vwc.Colour.user)]
        
    @staticmethod
    def init_agent(location, _type, minds):
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
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()])
        

class Dirt(Identifiable):
    
    def __init__(self, dirt):        
        super(Dirt, self).__init__()
        self._Identifiable__ID = dirt.name #hack...
        self.dirt = dirt

class ObservationProcess(Process):
    
    orientation_map = {vwc.Orientation.north:(0,-1),
                       vwc.Orientation.east:(1,0),
                       vwc.Orientation.south:(0,1),
                       vwc.Orientation.west:(-1,0)}

    def __call__(self, env):
        for agent in env.ambient.agents.values():
            env.physics.notify_agent(agent, ObservationProcess.get_perception(env.ambient.grid, agent))
        return []


    @staticmethod
    def get_perception(grid, agent):
        c = agent.coordinate
        f = ObservationProcess.orientation_map[agent.orientation]
        l = ObservationProcess.orientation_map[vwc.Direction.left(agent.orientation)]
        r = ObservationProcess.orientation_map[vwc.Direction.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = vwc.Observation(grid.state[c], 
                        grid.state[c + l],
                        grid.state[c + r], 
                        grid.state[c + f], 
                        grid.state[c + f + l],
                        grid.state[c + f + r])            
        return obs
