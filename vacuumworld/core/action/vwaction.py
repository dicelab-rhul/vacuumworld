from typing import Dict, Iterable, Tuple
from vacuumworld.core.environment.location_interface import Location
from vacuumworld.core.common.coordinates import Coord
from pystarworlds.Event import Action, Executor

from ..dirt.dirt_interface import Dirt
from ..common.orientation import Orientation
from ..common.direction import Direction
from ..common.colour import Colour
from ..common.message import Message
from ..action.action import move, turn, clean, drop, speak, idle
from ...utils.vwutils import VacuumWorldActionError, warn_agent

import copy


###################### action executors ###################### 

orientation_map: Dict[Orientation, Tuple[int, int]] = {Orientation.north:(0,-1),
                   Orientation.east:(1,0),
                   Orientation.south:(0,1),
                   Orientation.west:(-1,0)}


class MoveExecutor(Executor):
    def __call__(_, env, action) -> None:
        agent = env.ambient.agents[action.source]
        
        new_coordinate: Coord = agent.coordinate + orientation_map[agent.orientation]
        new_location: Location = env.ambient.grid.state[new_coordinate]
        #precondition
        if new_location and not new_location.agent:
            env.ambient.grid.move_agent(agent.coordinate, new_coordinate)
            agent.coordinate = new_coordinate


class TurnExecutor(Executor):
    def __call__(_, env, action) -> None:
        agent = env.ambient.agents[action.source]
        new_orientation = action.direction(agent.orientation)
        env.ambient.grid.turn_agent(agent.coordinate, new_orientation)
        agent.orientation = new_orientation


class CleanExecutor(Executor):
    def __call__(_, env, action) -> None:
        agent = env.ambient.agents[action.source]
        #precondition
        location = env.ambient.grid.state[agent.coordinate]
        if location.dirt and (location.agent.colour == location.dirt.colour or location.agent.colour == Colour.white):  
            dirt_id: str = location.dirt.name
            env.ambient.grid.remove_dirt(agent.coordinate)
            env.ambient.remove_dirt_from_list_of_dirts(dirt_id=dirt_id)


class DropExecutor(Executor):
    def __call__(_, env, action) -> None:
        agent = env.ambient.agents[action.source]
        #precondition
        if not env.ambient.grid.state[agent.coordinate].dirt:
            dirt_interface: Dirt = env.ambient.grid.dirt(action.colour)
            env.ambient.grid.place_dirt(agent.coordinate, dirt_interface)
            env.ambient.add_dirt_to_list_of_dirts(dirt=dirt_interface)


class CommunicativeExecutor(Executor):
    def __call__(_, env, action) -> None:
        notify: Iterable = action.to
        if len(notify) == 0: #send to everyone! do we want this?
            notify = set(env.ambient.agents.keys()) - set([action.source])
        for to in notify:
            env.physics.notify_agent(env.ambient.agents[to], Message(action.source, action.content))


###################### actions ###################### 
            
class VWPhysicalAction(Action):
     def __init__(self) -> None:
         super(VWPhysicalAction, self).__init__()


class MoveAction(VWPhysicalAction):
    executor = MoveExecutor


class CleanAction(VWPhysicalAction):
    executor = CleanExecutor


class DropAction(VWPhysicalAction):
    executor = DropExecutor
    
    def __init__(self, colour):
        super(DropAction, self).__init__()
        assert colour in [Colour.orange, Colour.green]
        self.colour = colour


class TurnAction(VWPhysicalAction):
    executor = TurnExecutor
    def __init__(self, direction):
        super(TurnAction, self).__init__()
        self.direction = direction


class CommunicativeAction(Action):
    executor = CommunicativeExecutor
    
    def __init__(self, content, *to):
        super(CommunicativeAction, self).__init__()
        self.content = content
        self.to = to


###################### create actions from label ###################### 

class ActionFactory():
    def __init__(_):
        # Useless
        pass
    
    def __call__(_):
        # Useless
        pass


class DropActionFactory(ActionFactory):
    def __init__(self):
        super(DropActionFactory, self).__init__()
        
    def __call__(_, _colour):
        return DropAction(_colour)
    
class TurnActionFactory(ActionFactory):
    def __init__(self):
        super(TurnActionFactory, self).__init__()
        
    def __call__(_, _direction):
        if not _direction in [Direction.left, Direction.right]:
            raise VacuumWorldActionError("{0} is not a valid direction for a turn action.\nValid directions are vwc.direction.left or vwc.direction.right".format(str(_direction)))
        return TurnAction(_direction)


class SpeakActionFactory(ActionFactory):
    LIMIT = 100
    
    def __init__(self):
        super(SpeakActionFactory, self).__init__()
        
    def __call__(self, _message, _to):
        self.__validate_message(_message)
        #create a deep copy to avoid possible reference cheating!
        _message = copy.deepcopy(_message) 
        _size = _message.size()
        if _size > SpeakActionFactory.LIMIT:
            _osize = _size
            _message, _size = self.__chop(_message)
            warn_agent("Agent: {0} message trimmed from {1} to {2}", _osize, _size) #todo refactor
        for t in _to:
            if type(t) != str:
                raise VacuumWorldActionError("Invalid recipient {0}, must be of type str".format(str(t)))
        return CommunicativeAction(_message, *_to)
    
    def __validate_message(self, message):
        if not type(message) in (str, int, float, bool, list, tuple, type(None)):
            raise VacuumWorldActionError("message content: {0} must be one of the following types (str, int, float, bool, list, tuple)".format(str(message)))
        if type(message) in (list, tuple, set):
            for e in message:
               self.__validate_message(e)
               
    def __chop(self, message):
        _size = message.size()

        while _size > SpeakActionFactory.LIMIT and type(message) in (list, tuple):
            if len(message) == 1:
                message = message[0]
                break
            message, _size = self.__chop(message[:-1])
        
        if message.size() > SpeakActionFactory.LIMIT:
            _t = type(message)
            message = _t(str(message)[:SpeakActionFactory.LIMIT])
            _size = message.size()
        return message, _size


action_factories: Dict[str, Action] = {
    move()[0]:lambda: MoveAction(), 
    clean()[0]:lambda: CleanAction(), 
    idle()[0]:lambda: None,
    turn(Direction.left)[0]: TurnActionFactory(), # TODO: the unused parameter is a dodgy choice.
    drop(Colour.green)[0]: DropActionFactory(),
    speak("")[0]: SpeakActionFactory()} # TODO: the unused parameter is a dodgy choice.
