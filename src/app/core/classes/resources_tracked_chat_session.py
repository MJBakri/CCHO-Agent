


from fastapi import WebSocket
from core.classes.abstract_classes.llm import LLM
from core.classes.chat_session import ChatSession


class ChatSessionWithTracker(ChatSession):
    def __init__(self, session_id:str, agent:LLM, ws_client:WebSocket):
        super().__init__(session_id=session_id, agent=agent, ws_client=ws_client)
        self.token_tracker = {
            "input_token":0,
            "output_token":0
        }
        
    def _add_consumed_resources(self, input_token: int, output_token: int):
        self.token_tracker['input_token'] += input_token
        self.token_tracker['output_token'] += output_token