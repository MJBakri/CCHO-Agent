from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMServiceProvider(ABC):

    @abstractmethod
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """An abstract class that represents an LLM service provider

        Args:
            api_key (Optional[str]): The API key for the service
        """
        self.api_key = api_key
        
    @abstractmethod
    def get_client(self,) -> 'LLMServiceProvider':
        """Returns the service client of the provider.
        """
        pass
