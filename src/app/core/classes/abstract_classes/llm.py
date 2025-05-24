from abc import ABC, abstractmethod
from typing import Optional


class LLM(ABC):
    
    context: Optional[str] = None
    
    @abstractmethod
    def __init__(
        self,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
        model_name: Optional[str] = None,
        **kwargs  # Allows additional parameters for flexibility
    ):
        """Initialize the LLM with generation parameters.

        Args:
            temperature (float): Controls randomness (lower = more deterministic).
            top_p (float): Controls diversity via nucleus sampling.
            max_tokens (Optional[int]): Maximum number of tokens to generate.
            model_name (Optional[str]): Name/identifier of the model.
            **kwargs: Additional model-specific parameters.
        """
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.model_name = model_name
        

    @abstractmethod
    def send_to_llm(self, message:str):
        """_summary_

        Args:
            message (str): _description_
        """
        pass
    
    def add_context(self, context: str):
        """Add context to the LLM instance.

        Args:
            context (str): Context to be added.
        """
        # This method can be overridden by subclasses if needed
        self.context = context