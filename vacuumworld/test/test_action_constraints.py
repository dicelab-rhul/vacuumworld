#!/usr/bin/env python3


import vacuumworld

from vacuumworld.vwc import action, direction

class TestMind():
    PATTERNS = {
            0: None, # no action
            1: action.move(), # single physical action without parameters.
            2: action.turn(direction.left), # single physical action with a single parameter.
            3: action.speak("Foo"), # single boradcasted speech with a simple string as the message.
            4: action.speak(["Foo", "Bar"]), # single boradcasted speech with a list of strings as the message.
            5: action.speak(["Foo", ("Bar", 1, ["2", 3])]), # single boradcasted speech with a complex data structure as the message.
            6: (action.move(), action.turn(direction.right)), # double physical action: MUST ERROR OUT.
            7: (action.speak(["Foo", ("Bar", 1, ["2", 3])]), action.speak(["Foo", ("Bar", 1, ["2", 3])])), # double speech: # MUST ERROR OUT.
            8: (action.move(), action.speak("Bar"), action.turn(direction.left)), # P, S, P --> MUST ERROR OUT.
            9: (action.speak("Foobar"), action.turn(direction.right), action.speak([1, 2, "3"])), # S, P, S --> MUST ERROR OUT.
            10: ["garbage"], # MUST ERROR OUT.
            11: "more_garbage", # MUST ERROR OUT.
            12: ("garbage", ["and", "garbage"]), # MUST ERROR OUT.
            13: (action.move(), "garbage"), # MUST ERROR OUT
            14: ("garbage", action.move()), # MUST ERROR OUT
            15: (action.move(), action.speak("foo"), ["garbage"]), # MUST ERROR OUT
            16: (action.speak("foo"), action.move(), ["garbage"]), # MUST ERROR OUT
            17: (["garbage"], action.speak("foo"), action.move()), # MUST ERROR OUT
            18: (action.speak("foo"), ["garbage"], action.move()), # MUST ERROR OUT
        }

    def __init__(self, pattern_number):
        super().__init__()
        self.grid_size = -1
        self.pattern_number = pattern_number

    def decide(self):
        return TestMind.PATTERNS[self.pattern_number]

    def revise(self, observation, messages):
        print(observation)
        print(messages)

for i in range(len(TestMind.PATTERNS)):
    print("\n########## Test #{} ##########\n".format(i))
    vacuumworld.run(TestMind(i), load="twins.vw")