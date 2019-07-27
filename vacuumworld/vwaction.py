from pystarworlds.Event import Action, Executor

from . import vwc

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
        if env.ambient.grid.state[agent.coordinate].dirt:  
            env.ambient.grid.remove_dirt(agent.coordinate)

class DropExecutor(Executor):
        
    def __call__(self, env, action):
        agent = env.ambient.agents[action.__actor__]
        #precondition
        if not env.ambient.grid.state[agent.coordinate].dirt:  
            env.ambient.grid.place_dirt(agent.coordinate, env.ambient.dirt(action.colour))
        
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
    
    def __init__(self):
        super(SpeakActionFactory, self).__init__()
        
    def __call__(self, _message, *_to):
        assert(isinstance(_message, str))
        for t in _to:
            #print(_actor, _message, _to)
            assert(isinstance(t, str))
        return CommunicativeAction(_message, *_to)
    
_action_factories = {'move':lambda: MoveAction(), 
                     'turn':TurnActionFactory(), 
                     'clean':lambda: CleanAction(), 
                     'drop':lambda: DropAction(),
                     'speak':SpeakActionFactory()}