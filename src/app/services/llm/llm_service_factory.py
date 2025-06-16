from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from services.llm.groq_llm import LLMGroq
from services.llm.clients.groq import groq_client
from core.classes.abstract_classes.llm_service_provider import LLMServiceProvider
from core.config import LLMProviders, settings

class LLMServiceFactory:
    @staticmethod
    def create_llm(provider: LLMProviders, **kwargs):
        """service
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
            return LLMGroq(**kwargs)
    

            
