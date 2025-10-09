#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vw_llm_actor_mind_surrogate import VWLLMActorMindSurrogate

from google.genai.types import GenerateContentResponse


class MyMind(VWLLMActorMindSurrogate):
    def __init__(self) -> None:
        # A `.env` file must be present in the same directory as this script, containing the GEMINI_API_KEY variable.
        super(MyMind, self).__init__(dot_env_path=".env")

        # Add here all the attributes you need/want.

    @override
    def revise(self) -> None:
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        print(f"Observation:\n{self.get_latest_observation().pretty_format()}")
        print(f"Messages: {[str(m) for m in self.get_latest_received_messages()]}")
        print(f"Current effort since the beginning of the simulation: {self.get_effort()}.")

    @override
    def decide(self) -> Iterable[VWAction]:
        # Replace this trivial decision process with something meaningful.
        return [self.decide_physical_with_ai(prompt="Unconditionally return 'VWIdleAction' (no quotes)."), VWBroadcastAction(message="Hello!", sender_id=self.get_own_id())]

    @override
    def parse_gemini_response(self, response: GenerateContentResponse) -> VWAction:
        # Parse the response from the Gemini model and return a valid VWAction.

        print(f"Gemini response: {response}")

        raise NotImplementedError("You must implement the parse_gemini_response method to parse the Gemini model's response and return a valid VWAction.")


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
