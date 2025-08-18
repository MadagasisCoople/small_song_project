import os 
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY") or ""
class ModelCilent:
    def generate_cilent(self, model_name:str ):
        model_client = OpenAIChatCompletionClient(
            model=model_name,
            api_key=OPEN_AI_KEY,
        )

        return model_client