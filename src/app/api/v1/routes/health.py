from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"

@router.get(
    "/", 
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the health status of the API"
)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc)
    )
