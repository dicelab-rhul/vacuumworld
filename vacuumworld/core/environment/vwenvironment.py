from typing import Dict, List, Set, Tuple, Type

from vacuumworld.core.environment.location_interface import Location
from vacuumworld.core.agent.agent_interface import Agent
from vacuumworld.core.common.coordinates import Coord
from vacuumworld.core.dirt.dirt_interface import Dirt as DirtInterface
from vacuumworld.core.environment.vw import Grid
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



def init(grid, minds: list, user_mind: int) -> "GridEnvironment":
    minds[Colour.user] = USERS[user_mind]()
    return GridEnvironment(GridAmbient(grid, minds))


class GridAmbient(Ambient):
    def __init__(self, grid: Grid, minds: list) -> None:
        self.grid: Grid = grid
        self.mind_types: Set[Type] = set(type(mind) for mind in minds)
        
        _agents: List[VWBody] = []
        _dirts: List[Dirt] = []

        for location in filter(lambda l: l is not None, grid.state.values()): 
            if location.agent:
                _agents.append(GridAmbient.init_agent(location, GridAmbient.get_type(location), minds))

            if location.dirt:
                _dirts.append(Dirt(location.dirt))

        super(GridAmbient, self).__init__(_agents, _dirts)
    
    @staticmethod
    def get_type(location: Location) -> str:
        return agent_type[int(location.agent.colour == Colour.user)]
        
    @staticmethod
    def init_agent(location: Location, _type: str, minds: dict) -> VWBody:
        return VWBody(_type, location.agent.name, copy.deepcopy(minds[location.agent.colour]), location.agent.orientation, location.coordinate, location.agent.colour)

    def remove_body_from_list_of_bodies(self, body_id: str) -> None:
        for b_id in self.agents:
            if b_id == body_id:
                del self.agents[body_id]
                break
    
    def add_dirt_to_list_of_dirts(self, dirt: DirtInterface) -> None:
        self.objects[dirt.name] = Dirt(dirt)

    def remove_dirt_from_list_of_dirts(self, dirt_id: str) -> None:
        for obj_id in self.objects:
            if obj_id == dirt_id:
                del self.objects[dirt_id]
                break


class GridPhysics(Physics):
    pass


class GridEnvironment(Environment):
    def __init__(self, ambient: GridAmbient) -> None:
        actions: List[Type] = [DropAction, MoveAction, TurnAction, CleanAction, CommunicativeAction]
        physics: GridPhysics = GridPhysics(actions)
        
        super(GridEnvironment, self).__init__(physics, ambient, [ObservationProcess()])


class ObservationProcess(Process):
    orientation_map: Dict[Orientation, Tuple[int, int]] = {
        Orientation.north:(0,-1),
        Orientation.east:(1,0),
        Orientation.south:(0,1),
        Orientation.west:(-1,0)
    }

    def __call__(_, env: GridEnvironment) -> list:
        for agent in env.ambient.agents.values():
            env.physics.notify_agent(agent, ObservationProcess.get_perception(env.ambient.grid, agent))
        return []

    @staticmethod
    def get_perception(grid: Grid, agent: Agent) -> Observation:
        c: Coord = agent.coordinate
        f: Tuple[int, int] = ObservationProcess.orientation_map[agent.orientation]
        l: Tuple[int, int] = ObservationProcess.orientation_map[Direction.left(agent.orientation)]
        r: Tuple[int, int] = ObservationProcess.orientation_map[Direction.right(agent.orientation)]
        #center left right forward forwardleft forwardright
        obs: Observation = Observation(grid.state[c], 
                        grid.state[c + l],
                        grid.state[c + r], 
                        grid.state[c + f], 
                        grid.state[c + f + l],
                        grid.state[c + f + r])            
        return obs
