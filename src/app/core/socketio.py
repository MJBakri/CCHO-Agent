import socketio
from fastapi import FastAPI
from logger.logger import logger
from core.classes.llm_service_factory import LLMServiceFactory
from core.config import settings
from services.llm.groq import groq_client
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[],
    # cors_allowed_origins=settings.CORS_ORIGINS,
    # path="/io",
    # logger=True,
    # ping_timeout=60,
    # ping_interval=25,
    # always_connect=True,
    # max_http_buffer_size=1e8
)



def setup_socketio(app: FastAPI):
    socket_app = socketio.ASGIApp(
        sio, 
        socketio_path=settings.SOCKETIO_PATH
        )
    app.mount(settings.SOCKETIO_MOUNT_LOCATION, socket_app)
    
    @sio.on('connect')
    async def connect(sid, environ):
        print(f"Client connected: {sid}")
        
        
    @sio.on('send_data')
    async def send_data(sid, environ):
        print(f"Client sent data: {sid}")
        print(f"environ: {environ}")
        llm_client = LLMServiceFactory.create_service("groq")
        
        chat_completion = await llm_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": environ,
                }
            ],
            model="llama3-8b-8192",
        )
        
        response = chat_completion.choices[0].message.content
        logger.debug(f"Responded: {response}")
            
        await sio.emit("echo_sent", response, to=sid)
       
    @sio.on('disconnect')
    async def disconnect(sid):
        print(f"Client disconnected: {sid}")