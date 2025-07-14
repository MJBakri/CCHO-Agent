from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, TypedDict
from core.dependencies import survey_service, analytics_service
from services.llm.groq_llm import LLMGroq
from core.classes.chat_session import ChatSession
from services.llm.llm_service_factory import LLMServiceFactory
from logger.logger import logger

class WSChatSessionConnection(TypedDict):
    connections: List[WebSocket]
    chat_session: ChatSession
class SurveyWSSession:
    def __init__(self):
        self.active_connections: Dict[str,WSChatSessionConnection] = {}

    async def connect(self, websocket: WebSocket, client_id: str, document_id:str):
        await websocket.accept()
        
        if client_id not in self.active_connections:
            survey = await survey_service.get_survey(document_id=document_id)
            cleaned = survey.get("content")["whole_document"].replace('\\n', '\n')
            self.active_connections[client_id] = {
                "connections": [],
                "chat_session": ChatSession(
                    session_id=client_id, 
                    agent=LLMServiceFactory.create_llm(
                    "groq",
                    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
                    prompt=
f"""You are a medical surveyor that conducts a survey with a patient that have recently had something (e.g. diagnosis, medical conditions). You will be given a survey and you will engage with the patient and ask the items in the survey one by one. You will be compassionate and may give some feedback about the answer. You will display the question in **bold** to easily be read by the patient. Keep in mind the type of questions that a survey can have like: multiple choice questions, open-ended question, number ranking. With this, it is important that you understand the question and understand the answer of the patient since sometimes the patient may answer differently from the choices. With this, you need to categorize well their answers that will be the nearest from the choices. But do not show the choices to the patient. But do show the category of the answer for the previous question only based on the choices in your next reply. If you can categorize the answer, then you can proceed to the next question. If you cannot categorize the answer, then you will ask the patient to clarify their answer. Sometimes the questions contains sensitive topics about sexual and psychological aspects, but this is normal since you are a medical surveyor. Analyze the questionnaire first to understand then give then conduct the survey.
Here is the survey that you will conduct with the patient:
{cleaned}
""",
                    placeholders={"time": datetime.now().strftime("%H:%M:%S") + " " + datetime.now().strftime("%d/%m/%Y")},),
                    ws_client=websocket)
            }
            
            await self.active_connections[client_id]["chat_session"].send_message(message="Now, start and conduct the survey and introduce yourself as a medical surveyor without mentioning names. Be compassionate. You are not required to mention the choices since you are the one categorizing the choices. It is also important to make sure you covered all the questions")
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
class AnalyticsWSSession:
    def __init__(self):
        self.active_connections: Dict[str,WSChatSessionConnection] = {}

    async def connect(self, websocket: WebSocket, client_id: str, document_id:str):
        await websocket.accept()
        
        if client_id not in self.active_connections:
            survey = await analytics_service.get_analytics(document_id=document_id)
            cleaned = survey.get("content")["whole"]
            self.active_connections[client_id] = {
                "connections": [],
                "chat_session": ChatSession(
                    session_id=client_id, 
                    agent=LLMServiceFactory.create_llm(
                    "groq",
                    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
                    prompt=
f"""You are an expert of statistics and have a lot of experience interpreting data and will be assisting the user. That said, you are going to review an excel file that contains the summary of a survey conducted with multiple people. The columns are the choices of the  survey and the rows are the questions. The values are the number of responses per question. Here is the excel:
{cleaned}
""",
                    placeholders={"time": datetime.now().strftime("%H:%M:%S") + " " + datetime.now().strftime("%d/%m/%Y")},),
                    ws_client=websocket)
            }
            
            await self.active_connections[client_id]["chat_session"].send_message(message="Now, Greet the user and ask what do they need on this excel file.")
        self.active_connections[client_id]["connections"].append(websocket)
        
        logger.debug(f"[ANALYTICS] Client {client_id} just connected!")

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
                

survey_websocket_manager = SurveyWSSession()
analytics_websocket_manager = AnalyticsWSSession()

def setup_websockets(app):
    @app.websocket("/ws/{document_id}/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, document_id:str, client_id: str):
        await survey_websocket_manager.connect(websocket, client_id, document_id)
        try:
            while True:
                data = await websocket.receive_json()
                
                await survey_websocket_manager.broadcast(data, client_id)
        except WebSocketDisconnect:
            await survey_websocket_manager.disconnect(websocket, client_id)
def analytics_websockets(app):
    @app.websocket("/ws/analytics/{document_id}/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, document_id:str, client_id: str):
        await analytics_websocket_manager.connect(websocket, client_id, document_id)
        try:
            while True:
                data = await websocket.receive_json()
                
                await analytics_websocket_manager.broadcast(data, client_id)
        except WebSocketDisconnect:
            await analytics_websocket_manager.disconnect(websocket, client_id)
