#!/usr/bin/env python3


from typing import Any, Dict, Iterable, Union
from vacuumworld.core.common.observation import Observation

from vacuumworld.core.action import action
from vacuumworld.core.common.direction import Direction as direction

import vacuumworld



class TestMind():
    PATTERNS: Dict[int, Any] = {
            0: None, # no action
            1: action.move(), # single physical action without parameters.
            2: action.turn(direction.left), # single physical action with a single parameter.
            3: action.speak("Foo"), # single boradcasted speech with a simple string as the message.
            4: action.speak(["Foo", "Bar"]), # single boradcasted speech with a list of strings as the message.
            5: action.speak(["Foo", ("Bar", 1, ["2", 3])]), # single boradcasted speech with a complex data structure as the message.
            6: (action.turn(direction.left), action.speak(["Foo", ("Bar", 1, ["2", 3])])), # P + S
            7: (action.speak(["Foo", ("Bar", 1, ["2", 3])]), action.turn(direction.right)), # S + P
            8: (action.move(), action.turn(direction.right)), # double physical action: MUST ERROR OUT.
            9: (action.speak(["Foo", ("Bar", 1, ["2", 3])]), action.speak(["Foo", ("Bar", 1, ["2", 3])])), # double speech: # MUST ERROR OUT.
            10: (action.move(), action.speak("Bar"), action.turn(direction.left)), # P, S, P --> MUST ERROR OUT.
            11: (action.speak("Foobar"), action.turn(direction.right), action.speak([1, 2, "3"])), # S, P, S --> MUST ERROR OUT.
            12: ["garbage"], # MUST ERROR OUT.
            13: "more_garbage", # MUST ERROR OUT.
            14: ("garbage", ["and", "garbage"]), # MUST ERROR OUT.
            15: (action.move(), "garbage"), # MUST ERROR OUT
            16: ("garbage", action.move()), # MUST ERROR OUT
            17: (action.move(), action.speak("foo"), ["garbage"]), # MUST ERROR OUT
            18: (action.speak("foo"), action.move(), ["garbage"]), # MUST ERROR OUT
            19: (["garbage"], action.speak("foo"), action.move()), # MUST ERROR OUT
            20: (action.speak("foo"), ["garbage"], action.move()), # MUST ERROR OUT
        }

    def __init__(self, pattern_number: int) -> None:
        super().__init__()
        self.grid_size: int = -1
        self.pattern_number: int = pattern_number

    def decide(self) -> Union[list, tuple]:
        return TestMind.PATTERNS[self.pattern_number]

    def revise(self, observation: Observation, messages: Iterable) -> None:
        self.observation: Observation = observation
        self.messages: Iterable = messages

        print(self.observation)
        print(self.messages)

for i in range(len(TestMind.PATTERNS)):
    print("\n########## Test #{} ##########\n".format(i))
    vacuumworld.run(default_mind=TestMind(i), load="full.vw", play=True)
