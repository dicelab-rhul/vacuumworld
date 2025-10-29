#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwactions import VWPhysicalAction
from vacuumworld.model.actions.vwactions import VWCommunicativeAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vw_llm_actor_mind_surrogate import VWLLMActorMindSurrogate

from google.genai.types import GenerateContentResponse
from google.genai.errors import ClientError


class MyMind(VWLLMActorMindSurrogate):
    def __init__(self) -> None:
        # A `.env` file must be present in the same directory as this script, containing the GEMINI_API_KEY variable.
        super(MyMind, self).__init__(dot_env_path=".env")

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
        return [self.decide_physical_with_ai(prompt="Unconditionally return 'VWIdleAction' (no quotes)."), VWBroadcastAction(message="Hello!", sender_id=self.get_own_id())]

    @override
    def backup_decide_after_llm_error(self, original_prompt: str, error: ClientError, action_superclass: type[VWPhysicalAction | VWCommunicativeAction]) -> VWAction:
        # Fallback decision process when an error occurs while querying the Gemini model.
        # Do something with the original prompt and the error, if needed.

        # For demonstration purposes, we will print the error details.
        # Remove if not needed, or use a proper logging mechanism.
        print(f"An error occurred while querying the Gemini model for a {action_superclass.__name__} with the prompt:\n{original_prompt}")
        print(f"Error details:\n{self.format_llm_error(error=error)}")

        # Return a default action as a fallback.
        return VWIdleAction()

    @override
    def parse_gemini_response(self, response: GenerateContentResponse) -> VWAction:
        # Parse the response from the Gemini model and return a valid VWAction.

        # For demonstration purposes, we will print the full response.
        # Remove if not needed, or use a proper logging mechanism.
        print(f"Gemini response:\n{self.format_llm_response_object(response=response)}")

        # For demonstration purposes, we will always return VWIdleAction.
        # In a real implementation, you would parse the response content to determine the appropriate action.
        return VWIdleAction()


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
