import types
from types import TracebackType
from typing import Any, List, Iterable, Tuple, Union
from vacuumworld.core.common.observation import Observation

from pystarworlds.Agent import Actuator, Mind

from .. import vwsensor
from ...action.action import speak, move, clean, idle, turn, drop
from ...action.vwaction import action_factories
from ...common.direction import Direction
from ...common.colour import Colour
from ....utils.vwutils import VacuumWorldActionError, ReturnFrame

from time import time_ns
from base64 import b64decode



class VWMind(Mind):
    MAX_NUMBER_OF_ACTIONS_PER_CYCLE: int = 2
    speech_actions: List[List[Union[str, list, tuple, int, float, bool, Iterable]]] = [speak("")]
    physical_actions: List[List[Union[str, Direction, Colour]]] = [idle(), move(), clean(), drop(Colour.green), turn(Direction.left)]
    actions: list = speech_actions + physical_actions

    def __init__(self, surrogate: Any, observers:list=[]) -> None:
        super(VWMind, self).__init__()
        self.surrogate: Any = surrogate
        self.observers: list = []

        for _ in observers:
            self.observers.append()
       
    def perceive(self) -> Tuple[Observation, Iterable]:
        observation: Observation = next(iter(self.body.perceive(vwsensor.VisionSensor.subscribe[0]).values()))
        assert(len(observation) == 1)
        
        messages: Iterable = next(iter(self.body.perceive(vwsensor.CommunicationSensor.subscribe[0]).values()))

        return observation, messages

    @staticmethod
    def validate_actions(actions: list) -> None:
        assert type(actions) == list

        # valid action formats:
        # (['a', ...],)
        # (['a',...],['b',...])
        # validate each action
        action_names: list = [a[0] for a in VWMind.actions]
        action_sizes: dict = {a[0]:len(a) for a in VWMind.actions}

        def validate_action(action):
            if action is None:
                return
            elif callable(action):
                raise VacuumWorldActionError("The action should not be a function name, did you forget the () - e.g. `move` in place of `move()` ?")
            elif type(action) != list or len(action) < 1:
                raise VacuumWorldActionError("Invalid action format: {}, please check the Wiki.".format(action))
            elif not action[0] in action_names:
                raise VacuumWorldActionError("Invalid action name: {}, please check the Wiki.".format(action))
            elif not len(action) == action_sizes[action[0]]:
                raise VacuumWorldActionError("Invalid (malformed) action: {}, please check the Wiki.".format(action))

        if len(actions) > VWMind.MAX_NUMBER_OF_ACTIONS_PER_CYCLE:
            raise VacuumWorldActionError("Too many actions for this cycle. There is a hard limit of 1 physical action (i.e., turn, move, clean, idle) and 1 communicative action (i.e., speak) per cycle.")

        for action in actions:
            validate_action(action)
        
        if len(actions) > 1:
            speech_action_names: list = [a[0] for a in VWMind.speech_actions]
            is_speech: List[bool] = [a[0] in speech_action_names for a in actions if a]
            if all(is_speech):
                raise VacuumWorldActionError("An agent can perform at most 1 communicative action (i.e., speak) per cycle.")
            
            physical_action_names = [a[0] for a in VWMind.physical_actions]
            is_physical: List[bool] = [a[0] in physical_action_names for a in actions if a]
            if all(is_physical):
                raise VacuumWorldActionError("An agent can perform at most 1 physical action (i.e., turn, move, clean, idle) per cycle.")

    def cycle(self) -> None:
        # For debug. Do not remove.
        if time_ns() % 7777 == 0:
            print()
            print(b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyIQ==").decode("utf-8"))
            print()

        observation, messages = self.perceive()

        self.surrogate.revise(*observation, messages)
        
        with ReturnFrame() as rf: # DO NOT PUT ANYTHING ELSE IN HERE - THIS IS DODGY DEBUG CODE 
            actions: Union[tuple, list] = self.surrogate.decide()
        
        if actions is None:
            return # No action

        if type(actions) == list:
            actions = (actions,)
        elif type(actions) != tuple:
            raise VacuumWorldActionError("Invalid action(s) format: {}, please check the Wiki.".format(actions))

        actions: list = [a for a in actions if a is not None]

        try:
            VWMind.validate_actions(actions)
            for action in actions:
                if action is not None and action != idle():
                    self.execute(action)
            
        except VacuumWorldActionError as vwe:
            tb: TracebackType = types.TracebackType(None, rf.frame, rf.frame.f_lasti, rf.frame.f_lineno)
            raise vwe.with_traceback(tb)

    def execute(self, action: Union[tuple, list]) -> None:
        assert action is not None

        _a = action_factories[action[0]](*action[1:])
        actuators: List[Actuator] = list(self.body.actuators.subscribed(type(_a)).values())
        
        if len(actuators) < 1:
            raise VacuumWorldActionError("No actuator found for action: {}".format(action))
        elif len(actuators) > 1:
            raise VacuumWorldActionError("Too many actuators (total = {}) found for action: {}".format(len(actuators), action))
        
        actuators[0].attempt(_a)
