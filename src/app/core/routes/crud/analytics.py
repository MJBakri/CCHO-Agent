from io import BytesIO
import json
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Query, UploadFile, status
from bson import json_util
from pdf2image import convert_from_bytes
from core.dependencies import analytics_service
from logger.logger import logger
from utils.json_converter import dict_bson_to_json
import base64
router = APIRouter()

@router.get("/analytics", tags=["Analytics"])
async def get_analytics():
    try:
        analytics = await analytics_service.get_analytics_collection()
        analytics_list = await analytics.to_list()  # Convert cursor to list properly
        
        logger.debug(f"Retrieved analytics: {analytics_list}")
        return {
            "analytics_list": dict_bson_to_json(analytics_list)  # Convert BSON to JSON
        }
        
    except Exception as e:
        logger.error(f"Error retrieving analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": str(e)
            }
        )
@router.get("/single-analytics", tags=["Analytics"])
async def get_single_analytics(document_id:str = Query(..., description="The document ID stored when the document is processed.")):
    try:
        analytics = await analytics_service.get_analytics(document_id=document_id)
        
        logger.debug(f"Retrieved analytics: {analytics}")
        return dict_bson_to_json(analytics)
        
    except Exception as e:
        logger.error(f"Error retrieving surveys: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": str(e)
            }
        )
        
@router.post("/add-analytics", tags=["Analytics"])
async def add_analytics(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None)
):
    try:
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": True,
                    "message": "Only Excel (xlsx) files are accepted"
                }
            )

        document_id = str(uuid4())
        file_content = await file.read()  # We need to read the file before the request ends
        
        # Add the processing task to background tasks
        
        analytics = await analytics_service.create_analytics(
            file_content=file_content,
            document_id=document_id,
            description=description,
            title=title or file.filename,
            file_name=file.filename
            )
        

        return {
            "message": "Analytics processed.",
            "document_id": document_id,
        }

    except Exception as e:
        logger.error(f"Error queuing survey: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": str(e)
            }
        )