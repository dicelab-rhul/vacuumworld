#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate


class MyMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    @override
    def revise(self) -> None:
        # Do something with the observation, the messages, and the effort, as needed.

        # For demonstration purposes, we will print perceptions and effort.
        # Remove if not needed, or use a proper logging mechanism.
        print(f"Observation:\n{self.get_latest_observation().pretty_format()}")
        print(f"Messages: {[str(m) for m in self.get_latest_received_messages()]}")
        print(f"Current effort since the beginning of the simulation: {self.get_effort()}.")

    @override
    def decide(self) -> Iterable[VWAction]:
        # Replace this trivial decision process with something meaningful.
        return [VWIdleAction(), VWBroadcastAction(message="Hello!", sender_id=self.get_own_id())]


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS, gui=False, load="files/guiless.json")
