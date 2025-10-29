from __future__ import annotations
from abc import abstractmethod
from typing import cast, Any
from json import loads, dumps
from google.genai.types import GenerateContentResponse
from google.genai.errors import ClientError

from pyoptional.pyoptional import PyOptional

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

    def provide_context(self, context: str) -> tuple[PyOptional[GenerateContentResponse], PyOptional[dict[str, Any]]]:
        '''
        Provides context to the Gemini model for generating a response.

        The `context` parameter is a string containing the context to be provided to the Gemini model.

        Returns a tuple where the first element is a `PyOptional` containing the `GenerateContentResponse` if the query was successful, or empty if an error occurred. The second element is a `PyOptional` containing a dictionary with error details if an error occurred, or empty if the query was successful.
        '''
        try:
            return PyOptional[GenerateContentResponse].of(self.__gemini_client.query(prompt=context)), PyOptional[dict[str, Any]].empty()
        except ClientError as ce:
            return PyOptional[GenerateContentResponse].empty(), PyOptional[dict[str, Any]].of(self.__format_llm_error(error=ce))

    def __decide_action_with_ai(self, prompt: str, action_superclass: type[VWPhysicalAction | VWCommunicativeAction]) -> VWAction:
        try:
            response: GenerateContentResponse = self.__gemini_client.query(prompt=prompt)
            action: VWAction = self.parse_gemini_response(response=response)

            assert action is not None and isinstance(action, VWAction), "The parsed action must be a valid VWAction."

            if isinstance(action, action_superclass):
                return action
            else:
                raise VWSurrogateMindException(f"The Gemini model did not return a valid {action_superclass.__name__}. Response: {response}")
        except ClientError as ce:
            return self.backup_decide_after_llm_error(original_prompt=prompt, error=ce, action_superclass=action_superclass)

    def decide_physical_with_ai(self, prompt: str) -> VWPhysicalAction:
        '''
        Uses the Gemini model to decide the next physical action to be performed by the `VWActor`, based on the given `prompt`.

        If an error occurs while querying the Gemini model, the `backup_decide_after_llm_error()` method is called to obtain a fallback action.
        '''
        return cast(VWPhysicalAction, self.__decide_action_with_ai(prompt=prompt, action_superclass=VWPhysicalAction))

    def decide_communicative_with_ai(self, prompt: str) -> VWCommunicativeAction:
        '''
        Uses the Gemini model to decide the next communicative action to be performed by the `VWActor`, based on the given `prompt`.

        If an error occurs while querying the Gemini model, the `backup_decide_after_llm_error()` method is called to obtain a fallback action.
        '''
        return cast(VWCommunicativeAction, self.__decide_action_with_ai(prompt=prompt, action_superclass=VWCommunicativeAction))

    @abstractmethod
    def backup_decide_after_llm_error(self, original_prompt: str, error: ClientError, action_superclass: type[VWPhysicalAction | VWCommunicativeAction]) -> VWAction:
        '''
        This method must be overridden by a subclass.

        It is called when an error occurs while querying the Gemini model.

        It must return a valid `VWPhysicalAction` or `VWCommunicativeAction` (according to the `action_superclass` argument) as a fallback decision.
        '''
        ...

    @abstractmethod
    def parse_gemini_response(self, response: GenerateContentResponse) -> VWAction:
        '''
        This method must be overridden by a subclass.

        Parses the `GenerateContentResponse` returned by the Gemini model and returns a valid `VWAction`.
        '''
        ...

    def format_llm_response_object(self, response: GenerateContentResponse) -> str:
        '''
        Formats the given `GenerateContentResponse` into a human-readable JSON string with proper indentation.

        This can be used to log or display response details.
        '''
        return dumps(loads(response.model_dump_json()), indent=4)

    def format_llm_error(self, error: ClientError) -> str:
        '''
        Formats the given `ClientError` into a human-readable JSON string with proper indentation.

        This can be used to log or display error details when handling LLM errors.
        '''
        return dumps(self.__format_llm_error(error=error), indent=4)

    def __format_llm_error(self, error: ClientError) -> dict[str, Any]:
        try:
            return {
                "code": error.code,
                "message": error.message,
                "status": error.status,
                "details": error.details,
                "response": {
                    "headers": dict(error.response.headers) if error.response else "N/A",
                    "status_code": error.response.status_code if error.response else "N/A",
                    "content": loads(error.response.text) if error.response else "N/A",
                }
            }
        except Exception:
            return {
                "code": error.code,
                "message": error.message,
                "status": error.status
            }
