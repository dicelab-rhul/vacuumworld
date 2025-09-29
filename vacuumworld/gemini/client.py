from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import GenerateContentResponse

import os


class GeminiClient():
    def __init__(self, model_name: str) -> None:
        self.__model_name: str = model_name

        self.__load_gemini_api_key()

        self.__client: Client = Client(api_key=os.environ["GEMINI_API_KEY"])

    def query(self, prompt: str) -> GenerateContentResponse:
        return self.__client.models.generate_content(model=self.__model_name, contents=prompt)

    def __load_gemini_api_key(self) -> None:
        try:
            load_dotenv()

            gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

            if not gemini_api_key:
                raise ValueError("No Gemini API key found.")

            os.environ["GEMINI_API_KEY"] = gemini_api_key
        except Exception as e:
            raise IOError(f"ERROR: Could not load Gemini API key. Please check the error message below.\n{e}\n")
