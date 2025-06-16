


from typing import Coroutine, List, Optional
from logger.logger import logger
from core.classes.message import ChatMessage, ChatRole


class ConversationManager:
    """A class that manages conversations and chat histories of users and AI."""
    
    

    
    def __init__(self, chat_session_id: str, messages: Optional[List[ChatMessage]]=None):
        self.chat_session_id = chat_session_id
        self.messages: List[ChatMessage] = []  # Now an instance variable
        if messages:
            self.messages.extend(messages)
            
    async def add_message(self, role:ChatRole, message:str, id:Optional[str]=None):
        """Add a message to the conversation history."""
        new_message = ChatMessage.create_message(role=role, message=message)
        self.messages.append(new_message)
        
    async def handle_ai_message(self, chunk: str, id: Optional[str] = None):
        """Handle an AI message by appending it to the conversation history."""
        if self.messages[-1].role != "assistant":
            new_message = ChatMessage.create_message(role="assistant", message=chunk, id=id)
            self.messages.append(new_message)
        else:
            await self.messages[-1].receive_ai_message(chars=chunk)
        
        
        
    async def get_messages(self)->List[ChatMessage]:
        """Get the conversation history."""
        return self.messages
    
    async def get_messages_to_llm(self, handler, **kwargs):
        """Get the conversation history formatted for LLM input."""
        message = []
        if callable(handler):
            
            prev_messages = [
            {
                "role": msg.role,
                "content": msg.get_latest_message()
            } for msg in self.messages
            ]
            
            message.extend([*prev_messages, *handler(**kwargs)])
        else:
            raise ValueError("Handler must be a function")
        
        return message