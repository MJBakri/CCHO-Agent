from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from services.llm.clients.groq import groq_client
from core.classes.abstract_classes.llm_service_provider import LLMServiceProvider
from core.config import LLMProviders, settings

class LLMServiceFactory:
    @staticmethod
    def create_service(provider: LLMProviders, config: Dict[str, Any]={}):
        """
        Create an LLM service instance based on the provider and configuration.
        
        Args:
            provider: The LLM provider ('openai' or 'azure_openai')
            config: Configuration dictionary with necessary credentials
        
        Returns:
            An instance of LLMService
        """
        
        if provider not in settings.SUPPORTED_LLM_PROVIDERS:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        if provider == "groq":
            return groq_client.get_client()
    

            
