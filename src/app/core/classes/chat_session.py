


from typing import Optional
from fastapi import WebSocket
from core.classes.abstract_classes.llm import LLM
from core.classes.conversation_manager import ConversationManager


class ChatSession:
    def __init__(self, session_id: str, agent:LLM, ws_client:Optional[WebSocket]=None):
        self.session_id = session_id
        self.conversation_manager = ConversationManager(chat_session_id=session_id, )
        self.agent = agent
        self.ws_client = ws_client

    async def _add_message(self, message: str):
        await self.conversation_manager.add_message(role="user", message=message)

    async def get_messages(self):
        return await self.conversation_manager.get_messages()
    
    async def send_message(self, message: str):
        await self._add_message(message)
        
        await self.agent.send_to_llm(message=message, ws_client=self.ws_client, conversation_manager=self.conversation_manager, stream=True)
