from abc import ABC, abstractmethod
from typing import List, Optional, Union

from fastapi import WebSocket

from core.classes.conversation_manager import ConversationManager
from core.classes.prompt import Prompt
from core.classes.context_manager import ContextManager
from models.llm.context import LLMContext


class LLM(ABC):
    
    @abstractmethod
    def __init__(
        self,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
        model_name: Optional[str] = None,
        prompt: Optional[str] = None,
        placeholders: dict={},
        **kwargs
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
        self.contexts = ContextManager()
        self.prompt = Prompt(prompt=prompt, placeholders=placeholders) if prompt else None

    @abstractmethod
    async def send_to_llm(self, message:str, ws_client:Optional[WebSocket]=None, conversation_manager:Optional[ConversationManager]=None) -> str:
        """A function to make a request to the LLM and return the response.
        Args:
            message (str): The message to send to the LLM.
            ws_client (Optional[WebSocket]): WebSocket client for real-time communication.
            conversation_manager (Optional[ConversationManager]): Conversation manager for context.

        """
        pass
    
    @abstractmethod
    def resources_recorder(self):
        pass
    
    def add_context(self, context: Union[LLMContext, List[LLMContext]]):
        """Add context to the LLM instance.

        Args:
            context (str): Context to be added.
        """
        
        self.contexts.add_context(context)
        
