from warnings import warn

from pystarworlds.Event import Action, Executor
from . import vwc
from . import vwutils

###################### action executors ###################### 

class MoveExecutor(Executor):
    
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        
        new_coordinate = agent.coordinate + vwc.orientation_map[agent.orientation]
        new_location = env.ambient.grid.state[new_coordinate]
        #precondition
        if new_location and not new_location.agent:
            env.ambient.grid.move_agent(agent.coordinate, new_coordinate)
            agent.coordinate = new_coordinate
        
class TurnExecutor(Executor):
         
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        new_orientation = action.direction(agent.orientation)
        env.ambient.grid.turn_agent(agent.coordinate, new_orientation)
        agent.orientation = new_orientation

class CleanExecutor(Executor):
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        #precondition
        location = env.ambient.grid.state[agent.coordinate]
        if location.dirt and (location.agent.colour == location.dirt.colour or location.agent.colour == vwc.colour.white):  
            env.ambient.grid.remove_dirt(agent.coordinate)
            #TODO remove dirt from list of objects in ambient

class DropExecutor(Executor):
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        #precondition
        if not env.ambient.grid.state[agent.coordinate].dirt: 

            env.ambient.grid.place_dirt(agent.coordinate, env.ambient.grid.dirt(action.colour))
            #location = env.ambient.grid.state[agent.coordinate]
           
            #TODO add new dirt to list of objects in ambient
        
class CommunicativeExecutor(Executor):

    def __call__(self, env, action):
        notify = action.to
        if len(notify) == 0: #send to everyone! do we want this?
            notify = set(env.ambient.agents.keys()) - set([action.__actor__])
        for to in notify:
            env.physics.notify_agent(env.ambient.agents[to], vwc.message(action.__actor__, action.content))
            
###################### actions ###################### 
            
class VWPhysicalAction(Action):
     def __init__(self):
         super(VWPhysicalAction, self).__init__()
    
class MoveAction(VWPhysicalAction):
    executor = MoveExecutor
    pass
             
class CleanAction(VWPhysicalAction):
    executor = CleanExecutor
    pass

class DropAction(VWPhysicalAction):
    executor = DropExecutor
    
    def __init__(self, colour):
        super(DropAction, self).__init__()
        assert colour in vwc._colour_dirt
        self.colour = colour
        
class TurnAction(VWPhysicalAction):
    executor = TurnExecutor
    def __init__(self, direction):
        super(TurnAction, self).__init__()
        assert direction in vwc.direction
        self.direction = direction

class CommunicativeAction(Action):
    executor = CommunicativeExecutor
    
    def __init__(self, content, *to):
        super(CommunicativeAction, self).__init__()
        self.content = content
        self.to = to

###################### create actions from label ###################### 

class ActionFactory:
    
    def __init__(self):
        pass
    
    def __call__(self):
        pass
    
class DropActionFactory(ActionFactory):
    
    def __init__(self):
        super(DropActionFactory, self).__init__()
        
    def __call__(self, _colour):
        return DropAction(_colour)
    
class TurnActionFactory(ActionFactory):
    
    def __init__(self):
        super(TurnActionFactory, self).__init__()
        
    def __call__(self, _direction):
        return TurnAction(_direction)
    
class SpeakActionFactory(ActionFactory):
    
    LIMIT = 100
    
    def __init__(self):
        super(SpeakActionFactory, self).__init__()
        
    def __call__(self, _message, *_to):
        self.__validate_message(_message)
        _size = vwc.size(_message)
        if _size > SpeakActionFactory.LIMIT:
            _osize = _size
            _message, _size = self.__chop(_message)
            vwutils.warn_agent("Agent: {0} message trimmed from {1} to {2}", _osize, _size)
        for t in _to:
            assert(isinstance(t, str))
        return CommunicativeAction(_message, *_to)
    
    def __validate_message(self, message):
        assert(type(message) in (str, int, float, bool, list, tuple, type(None)))
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

_action_factories = {vwc.move.__name__:lambda: MoveAction(), 
                     vwc.clean.__name__:lambda: CleanAction(), 
                     vwc.idle.__name__:lambda: None,
                     vwc.turn.__name__:TurnActionFactory(), 
                     vwc.drop.__name__:DropActionFactory(),
                     vwc.speak.__name__:SpeakActionFactory()}



    
    