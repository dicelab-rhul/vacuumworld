import sys
import traceback
import types

from pystarworlds.Agent import Mind, Body

from . import vwsensor
from . import vwactuator
from . import vwagent 
from . import vwaction
from . import vwc
from . import vwutils


from collections import namedtuple
agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')

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
    
    MAX_NUMBER_OF_ACTIONS_PER_CYCLE = 2
    speech_actions   = [vwc.action.speak("")]
    physical_actions = [vwc.action.idle(), vwc.action.move(), vwc.action.clean(), vwc.action.drop(vwc.colour.green), vwc.action.turn(vwc.direction.left)]
    actions = speech_actions + physical_actions

    def __init__(self, surrogate, observers = []):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
        self.observers = []
        for _ in observers:
            self.observers.append()
       
    def perceive(self):
        observation = next(iter(self.body.perceive(vwsensor.VisionSensor.subscribe[0]).values()))
        assert(len(observation) == 1)
        
        messages = next(iter(self.body.perceive(vwsensor.CommunicationSensor.subscribe[0]).values()))

        return observation, messages

    @staticmethod
    def validate_actions(actions):
        assert type(actions) == list

        # valid action formats:
        # (['a', ...],)
        # (['a',...],['b',...])
        # validate each action
        action_names = [a[0] for a in VWMind.actions]
        action_sizes = {a[0]:len(a) for a in VWMind.actions}

        def validate_action(action):
            if action is None:
                return
            elif callable(action):
                raise vwutils.VacuumWorldActionError("Action should not be a function name, did you forget the ()? - e.g. action.move()")
            elif type(action) != list or len(action) < 1:
                raise vwutils.VacuumWorldActionError("Invalid action format: {}, please use vwc.action".format(action))
            elif not action[0] in action_names:
                raise vwutils.VacuumWorldActionError("Invalid action name: {}, please use vwc.action".format(action))
            elif not len(action) == action_sizes[action[0]]:
                raise vwutils.VacuumWorldActionError("Invalid (malformed) action: {}, please use vwc.action".format(action))

        if len(actions) > VWMind.MAX_NUMBER_OF_ACTIONS_PER_CYCLE:
            raise vwutils.VacuumWorldActionError("Too many actions for this cycle. There is a hard limit of 1 physical action and 1 speech per cycle.")

        for action in actions:
            validate_action(action)
        
        if len(actions) > 1:
            speech_action_names = [a[0] for a in VWMind.speech_actions]
            is_speech = [a[0] in speech_action_names for a in actions if a]
            if all(is_speech):
                raise vwutils.VacuumWorldActionError("An agent can perform at most 1 speech action per cycle (vwc.action.speak)")
            
            physical_action_names = [a[0] for a in VWMind.physical_actions]
            is_physical =  [a[0] in physical_action_names for a in actions if a]
            if all(is_physical):
                raise vwutils.VacuumWorldActionError("An agent can perform at most 1 physical action per cycle (vwc.action.clean, move, turn, idle)")

    def cycle(self):

        observation, messages = self.perceive()

        self.surrogate.revise(*observation, messages)
        
        with vwutils.ReturnFrame() as rf: # DO NOT PUT ANYTHING ELSE IN HERE - THIS IS DODGY DEBUG CODE 
            actions = self.surrogate.decide()
        
        if actions is None:
            return # No action

        if type(actions) == list:
            actions = (actions,)
        else:
            raise vwutils.VacuumWorldActionError("Invalid action(s) format: {}, please use vwc.action".format(actions))

        actions = [a for a in actions if a is not None]

        try:
            VWMind.validate_actions(actions)
            for action in actions:
                if action is not None:
                    self.execute(action)
            
        except vwutils.VacuumWorldActionError as vwe:
            tb = types.TracebackType(None, rf.frame, rf.frame.f_lasti, rf.frame.f_lineno)
            raise vwe.with_traceback(tb)

    def execute(self, action):
        assert action is not None

        _a = vwaction._action_factories[action[0]](*action[1:])
        actuators = list(self.body.actuators.subscribed(type(_a)).values())
        
        if len(actuators) < 1:
            raise vwutils.VacuumWorldActionError("No actuator found for action: {}".format(action))
        elif len(actuators) > 1:
            raise vwutils.VacuumWorldActionError("Too many actuators found for action: {}".format(action))
        
        actuators[0].attempt(_a)
