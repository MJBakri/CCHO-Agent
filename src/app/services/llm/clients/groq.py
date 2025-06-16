from dotenv import load_dotenv
import os
from groq import AsyncGroq
from core.classes.abstract_classes.llm_service_provider import LLMServiceProvider

load_dotenv()

class GroqService(LLMServiceProvider):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required for Groq LLM")
        super().__init__(api_key=api_key)
        self.client = AsyncGroq(api_key=self.api_key)
        
    def get_client(self) -> AsyncGroq:
        return self.client
    
groq_client = GroqService(
    api_key=os.getenv("GROQ_API_KEY")
)
    
    
        