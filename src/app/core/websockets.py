from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
from core.classes.llm_service_factory import LLMServiceFactory
from logger.logger import logger
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        logger.debug(f"Client {client_id} just connected!")

    async def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]

    async def broadcast(self, payload: dict, client_id: str):
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                message = payload.get("message")
                logger.debug(f"Received Message: {message}")
                llm_client = LLMServiceFactory.create_service("groq")
                
                stream = await llm_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant.",
                        },
                        {
                            "role": "user",
                            "content": message,
                        },
                    ],
                    model="llama3-8b-8192",
                    stream=True
                )

                async for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        await connection.send_json({"reply":chunk.choices[0].delta.content})

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
