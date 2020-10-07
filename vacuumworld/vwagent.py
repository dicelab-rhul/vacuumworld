from pystarworlds.Agent import Mind, Body

from . import vwsensor
from . import vwactuator
from . import vwagent 
from . import vwaction
from . import vwc
from . import vwutils

from enum import Enum

from collections import namedtuple
agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')


class ActionFlow(Enum):
    SINGLE = 0
    DOUBLE = 1
    NONE = 2

class VWBody(Body):
    def __init__(self, _type, id, mind, orientation, coordinate, colour):
        mind = vwagent.VWMind(mind)
        assert _type in agent_type
        if _type == agent_type.cleaning:
            actuators = [vwactuator.CleaningAgentActuator(), vwactuator.CommunicationActuator()]
        else:
            actuators = [vwactuator.UserActuator(), vwactuator.CommunicationActuator()]

        sensors = [vwsensor.VisionSensor(), vwsensor.CommunicationSensor()]
        self._Identifiable__ID = id #hack...
        
        super(VWBody, self).__init__(mind, actuators, sensors)
        
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate

class VWMind(Mind):
    
    action_names = [vwc.action.move.__name__, vwc.action.clean.__name__, vwc.action.idle.__name__,
                    vwc.action.drop.__name__, vwc.action.turn.__name__, vwc.action.speak.__name__]
    speech_action_names = [vwc.action.speak.__name__]
    physical_action_names =  [vwc.action.move.__name__, vwc.action.clean.__name__,
                              vwc.action.drop.__name__, vwc.action.turn.__name__]
    action_size = {vwc.action.move.__name__:1, vwc.action.clean.__name__:1, vwc.action.idle.__name__:1,
                   vwc.action.drop.__name__:2, vwc.action.turn.__name__:2, vwc.action.speak.__name__:3}

    MAX_ACTION_SIZE = max(action_size.values())
    
    def __init__(self, surrogate, observers = []):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
        self.observers = []
        for _ in observers:
            self.observers.append()
       
    def _do_perceive(self):
        observation = next(iter(self.body.perceive(vwsensor.VisionSensor.subscribe[0]).values()))
        assert(len(observation) == 1)
        
        messages = next(iter(self.body.perceive(vwsensor.CommunicationSensor.subscribe[0]).values()))

        return observation, messages

    @staticmethod
    def _get_action_flow_type(actions):
        assert actions
        
        if type(actions) != tuple:
            raise vwutils.VacuumWorldActionError("Invalid action(s): {}, please use vwc.action".format(str(actions)))

        actions = tuple([action for action in actions if action is not None])

        if len(actions) == 0:
            return ActionFlow.NONE, actions
        elif len(actions) <= VWMind.MAX_ACTION_SIZE and type(actions[0]) == str:
            return ActionFlow.SINGLE, actions
        elif len(actions) == 2 and type(actions[0]) == tuple and type(actions[1] == tuple):
            return ActionFlow.DOUBLE, actions
        elif len(actions) > 2:
            raise vwutils.VacuumWorldActionError("Invalid action(s): {}, an agent can perform at most 1 physical action and 1 speech action per cycle (a total of 2 actions)".format(str(actions)))
        else:
            raise vwutils.VacuumWorldActionError("Invalid action(s): {}, please use vwc.action".format(str(actions)))

    def _validate_and_execute_actions(self, actions):
        action_flow_type, actions = VWMind._get_action_flow_type(actions)

        if action_flow_type == ActionFlow.SINGLE:
            self.attempt_action(VWMind.validate_action(actions))
        elif action_flow_type == ActionFlow.DOUBLE:
            actions = [VWMind.validate_action(action) for action in actions]
            names = [action[0] for action in actions]
            is_speech = [name in VWMind.speech_action_names for name in names]
            is_physical = [name in VWMind.physical_action_names for name in names]
            
            if all(is_speech):
                raise vwutils.VacuumWorldActionError("An agent can perform at most 1 speech action per cycle (vwc.action.speak)")
            
            if all(is_physical):
                raise vwutils.VacuumWorldActionError("An agent can perform at most 1 physical action per cycle (vwc.action.clean, move, turn, idle, drop)")
            
            for action in actions:
                self.attempt_action(action)
        elif action_flow_type == ActionFlow.NONE:
            return # No action
        else:
            raise ValueError("This should not be reachable.")

    def cycle(self):
        # Perceive
        observation, messages = self._do_perceive()

        # Revise
        self.surrogate.revise(*observation, messages)
    
        # Decide
        actions = self.surrogate.decide()
        #https://pymotw.com/2/sys/tracing.html
        #to get helpful exception information it will be better to trace decide!

        # Execute
        if actions is None:
            return # No action
        else:
            self._validate_and_execute_actions(actions)
    
    def attempt_action(self, action):
        _a = vwaction._action_factories[action[0]](*action[1:])
        if _a is None: #idle action
            return 
        actuators = list(self.body.actuators.subscribed(type(_a)).values())
        if len(actuators) != 1:
            raise vwutils.VacuumWorldActionError("No actuator found for action: " + str(action))
        actuators[0].attempt(_a)
        
    @staticmethod
    def validate_action(action):
        if type(action) == tuple:
            if len(action) > 0 and action[0] in VWMind.action_names and len(action) == VWMind.action_size[action[0]]:
                return action
        elif callable(action):
            raise vwutils.VacuumWorldActionError("Action should not be a function, did you forget the ()? - e.g. action.move()")
        raise vwutils.VacuumWorldActionError("Invalid action: {} please use vwc.action.".format(str(action)))
