from pystarworlds.Event import Action, Executor
from . import vwc
from .vwutils import VacuumWorldActionError, warn_agent

import copy


###################### action executors ###################### 

orientation_map = {vwc.Orientation.north:(0,-1),
                   vwc.Orientation.east:(1,0),
                   vwc.Orientation.south:(0,1),
                   vwc.Orientation.west:(-1,0)}


class MoveExecutor(Executor):
    def __call__(_, env, action):
        agent = env.ambient.agents[action.source]
        
        new_coordinate = agent.coordinate + orientation_map[agent.orientation]
        new_location = env.ambient.grid.state[new_coordinate]
        #precondition
        if new_location and not new_location.agent:
            env.ambient.grid.move_agent(agent.coordinate, new_coordinate)
            agent.coordinate = new_coordinate


class TurnExecutor(Executor): 
    def __call__(_, env, action):
        agent = env.ambient.agents[action.source]
        new_orientation = action.direction(agent.orientation)
        env.ambient.grid.turn_agent(agent.coordinate, new_orientation)
        agent.orientation = new_orientation


class CleanExecutor(Executor):
    def __call__(_, env, action):
        agent = env.ambient.agents[action.source]
        #precondition
        location = env.ambient.grid.state[agent.coordinate]
        if location.dirt and (location.agent.colour == location.dirt.colour or location.agent.colour == vwc.Colour.white):  
            env.ambient.grid.remove_dirt(agent.coordinate)
            #TODO: remove dirt from list of objects in ambient


class DropExecutor(Executor):
    def __call__(_, env, action):
        agent = env.ambient.agents[action.source]
        #precondition
        if not env.ambient.grid.state[agent.coordinate].dirt: 
            env.ambient.grid.place_dirt(agent.coordinate, env.ambient.grid.dirt(action.colour))
           
            #TODO: add new dirt to list of objects in ambient


class CommunicativeExecutor(Executor):
    def __call__(_, env, action):
        notify = action.to
        if len(notify) == 0: #send to everyone! do we want this?
            notify = set(env.ambient.agents.keys()) - set([action.source])
        for to in notify:
            env.physics.notify_agent(env.ambient.agents[to], vwc.Message(action.source, action.content))


###################### actions ###################### 
            
class VWPhysicalAction(Action):
     def __init__(self):
         super(VWPhysicalAction, self).__init__()


class MoveAction(VWPhysicalAction):
    executor = MoveExecutor


class CleanAction(VWPhysicalAction):
    executor = CleanExecutor


class DropAction(VWPhysicalAction):
    executor = DropExecutor
    
    def __init__(self, colour):
        super(DropAction, self).__init__()
        assert colour in [vwc.Colour.orange, vwc.Colour.green]
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
        if not _direction in [vwc.Direction.left, vwc.Direction.right]:
            print([vwc.Direction.left, vwc.Direction.right])
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
        _size = vwc.size(_message)
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
        _size = vwc.size(message)

        while _size > SpeakActionFactory.LIMIT and type(message) in (list, tuple):
            if len(message) == 1:
                message = message[0]
                break
            message, _size = self.__chop(message[:-1])
        
        if vwc.size(message) > SpeakActionFactory.LIMIT:
            _t = type(message)
            message = _t(str(message)[:SpeakActionFactory.LIMIT])
            _size = vwc.size(message)
        return message, _size

#TODO: why is this never accessed locally?
_action_factories = {vwc.action.move()[0]:lambda: MoveAction(), 
                     vwc.action.clean()[0]:lambda: CleanAction(), 
                     vwc.action.idle()[0]:lambda: None,
                     vwc.action.turn(vwc.direction.left)[0]:TurnActionFactory(), 
                     vwc.action.drop(vwc.colour.green)[0]:DropActionFactory(),
                     vwc.action.speak("")[0]:SpeakActionFactory()}
