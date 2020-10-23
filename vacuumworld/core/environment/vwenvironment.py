from ..common.colour import Colour
from ..common.orientation import Orientation
from ..common.direction import Direction
from ..common.observation import Observation
from ..agent.vwagent import VWBody, agent_type
from ..user.vwuser import USERS
from ..dirt.vwdirt import Dirt
from ..action.vwaction import CommunicativeAction, MoveAction, TurnAction, CleanAction, DropAction

from pystarworlds.Environment import Ambient, Physics, Environment, Process

import copy



def init(grid, minds, user_mind):
    minds[Colour.user] = USERS[user_mind]()
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
        return agent_type[int(location.agent.colour == Colour.user)]
        
    @staticmethod
    def init_agent(location, _type, minds):
        return VWBody(_type, location.agent.name, copy.deepcopy(minds[location.agent.colour]), location.agent.orientation, location.coordinate, location.agent.colour)
        

class GridPhysics(Physics):
    pass


class GridEnvironment(Environment):
    def __init__(self, ambient):
        
        actions = [DropAction, MoveAction, TurnAction, CleanAction, CommunicativeAction]
        
        physics = GridPhysics(actions)
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()])


class ObservationProcess(Process):
    orientation_map = {
        Orientation.north:(0,-1),
        Orientation.east:(1,0),
        Orientation.south:(0,1),
        Orientation.west:(-1,0)
    }

    def __call__(_, env):
        for agent in env.ambient.agents.values():
            env.physics.notify_agent(agent, ObservationProcess.get_perception(env.ambient.grid, agent))
        return []


    @staticmethod
    def get_perception(grid, agent):
        c = agent.coordinate
        f = ObservationProcess.orientation_map[agent.orientation]
        l = ObservationProcess.orientation_map[Direction.left(agent.orientation)]
        r = ObservationProcess.orientation_map[Direction.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs = Observation(grid.state[c], 
                        grid.state[c + l],
                        grid.state[c + r], 
                        grid.state[c + f], 
                        grid.state[c + f + l],
                        grid.state[c + f + r])            
        return obs
