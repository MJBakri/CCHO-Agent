from fastapi import FastAPI
from core.lifespan import lifespan
from logger.logger import logger
from core.config import settings
from api.v1.api import api_router
from core.middleware import setup_middleware
from core.websockets import setup_websockets
from core.routes.crud.surveys import router as surveys_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

setup_middleware(app)
# setup_socketio(app)  # Socket.IO setup
setup_websockets(app)  # WebSocket setup

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(surveys_router, prefix=settings.API_V1_STR)


