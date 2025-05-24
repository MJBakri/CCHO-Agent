from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, TypedDict
from services.llm.groq_llm import LLMGroq
from core.classes.chat_session import ChatSession
from services.llm.llm_service_factory import LLMServiceFactory
from logger.logger import logger

class WSChatSessionConnection(TypedDict):
    connections: List[WebSocket]
    chat_session: ChatSession
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str,WSChatSessionConnection] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = {
                "connections": [],
                "chat_session": ChatSession(session_id=client_id, agent=LLMGroq(
                    model_name="llama3-8b-8192",
                    prompt="Always start your response with a Greeting and time. This is the context for time: {time}",
                    placeholders={"time": datetime.now().strftime("%H:%M:%S") + " " + datetime.now().strftime("%d/%m/%Y")},
                ), ws_client=websocket)
            }
        self.active_connections[client_id]["connections"].append(websocket)
        
        logger.debug(f"Client {client_id} just connected!")

    async def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id]["connections"].remove(websocket)
            if not self.active_connections[client_id]["connections"]:
                del self.active_connections[client_id]

    async def broadcast(self, payload: dict, client_id: str):
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]["connections"]:
                message = payload.get("message")
                logger.debug(f"Received Message: {message}")
                chat_session = self.active_connections[client_id]["chat_session"]
                cs = await chat_session.send_message(message=message)
                ct = await chat_session.get_messages()
                logger.debug(f"ChatHistory: {ct}")
                

websocket_manager = WebSocketManager()

def setup_websockets(app):
    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await websocket_manager.connect(websocket, client_id)
        try:
            while True:
                data = await websocket.receive_json()
                
                await websocket_manager.broadcast(data, client_id)
        except WebSocketDisconnect:
            await websocket_manager.disconnect(websocket, client_id)
