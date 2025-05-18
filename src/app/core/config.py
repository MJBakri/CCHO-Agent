from typing import List, Literal
from pydantic_settings import BaseSettings


LLMProviders = Literal["groq"]
supported_llm_providers = ["groq"]

class Settings(BaseSettings):
    PROJECT_NAME: str = "CCHO-AGENT"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "Unlock deeper insights with CCHO-AGENT, the intelligent API designed to power next-generation medical research. Like a precision probe (sonde) into the collective mind of healthcare data, CCHO-AGENT collects, analyzes, and structures survey responses with clinical accuracy—turning raw feedback into actionable intelligence."
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = ""
    SOCKETIO_MOUNT_LOCATION: str = "/ws/main"
    SOCKETIO_PATH: str = "/ws" 
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    SUPPORTED_LLM_PROVIDERS: List[LLMProviders] = supported_llm_providers


    class Config:
        env_file = ".env"

settings = Settings()
