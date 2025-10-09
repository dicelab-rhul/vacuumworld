from __future__ import annotations
from abc import abstractmethod
from google.genai.types import GenerateContentResponse

from .vwactor_mind_surrogate import VWActorMindSurrogate
from ....actions.vwactions import VWAction
from ....actions.vwactions import VWPhysicalAction
from ....actions.vwactions import VWCommunicativeAction
from ....environment.vwenvironment import VWEnvironment
from .....common.vwexceptions import VWSurrogateMindException
from .....gemini.client import GeminiClient

import os
import sys


class VWLLMActorMindSurrogate(VWActorMindSurrogate):
    '''
    This class specifies an LLM-capable surrogate for the `VWMind` of a `VWActor` that uses a Gemini model to decide the next actions to be performed by the `VWActor`.
    '''

    def __init__(self, dot_env_path: str) -> None:
        super(VWLLMActorMindSurrogate, self).__init__()

        under_pytest = "pytest" in sys.modules or os.getenv("PYTEST_CURRENT_TEST") is not None or os.getenv("PYTEST_XDIST_WORKER") is not None
        skip_gemini_setup: bool = under_pytest or os.getenv("VW_SKIP_AI_SETUP", "").strip().lower() in {"1", "true", "yes", "on"}

        if not skip_gemini_setup:
            self.__gemini_client: GeminiClient = GeminiClient(model_name=VWEnvironment.LLM_MODEL, dot_env_path=dot_env_path)

    def provide_context(self, context: str) -> GenerateContentResponse:
        return self.__gemini_client.query(prompt=context)

    def decide_physical_with_ai(self, prompt: str) -> VWPhysicalAction:
        response: GenerateContentResponse = self.__gemini_client.query(prompt=prompt)
        action: VWAction = self.parse_gemini_response(response=response)

        if isinstance(action, VWPhysicalAction):
            return action
        else:
            raise VWSurrogateMindException(f"The Gemini model did not return a valid VWPhysicalAction. Response: {response}")

    def decide_communicative_with_ai(self, prompt: str) -> VWCommunicativeAction:
        response: GenerateContentResponse = self.__gemini_client.query(prompt=prompt)
        action: VWAction = self.parse_gemini_response(response=response)

        if isinstance(action, VWCommunicativeAction):
            return action
        else:
            raise VWSurrogateMindException(f"The Gemini model did not return a valid VWCommunicativeAction. Response: {response}")

    @abstractmethod
    def parse_gemini_response(self, response: GenerateContentResponse) -> VWAction:
        '''
        This method must be overridden by a subclass.

        Parses the `GenerateContentResponse` returned by the Gemini model and returns a valid `VWAction`.
        '''
        ...
