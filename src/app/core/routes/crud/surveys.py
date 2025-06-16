from io import BytesIO
import json
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Query, UploadFile, status
from bson import json_util
from pdf2image import convert_from_bytes
from core.dependencies import survey_service
from logger.logger import logger
from utils.json_converter import dict_bson_to_json
import base64
router = APIRouter()

@router.get("/surveys", tags=["Surveys"])
async def get_surveys():
    try:
        surveys = await survey_service.get_surveys()
        survey_list = await surveys.to_list()  # Convert cursor to list properly
        
        logger.debug(f"Retrieved surveys: {survey_list}")
        return {
            "survey_list": dict_bson_to_json(survey_list)  # Convert BSON to JSON
        }
        
    except Exception as e:
        logger.error(f"Error retrieving surveys: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": str(e)
            }
        )
@router.get("/survey", tags=["Surveys"])
async def get_survey(document_id:str = Query(..., description="The document ID stored when the document is processed.")):
    try:
        surveys = await survey_service.get_survey(document_id=document_id)
        
        logger.debug(f"Retrieved survey: {surveys}")
        return dict_bson_to_json(surveys)
        
    except Exception as e:
        logger.error(f"Error retrieving surveys: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": str(e)
            }
        )
        
@router.post("/add-survey", tags=["Surveys"])
async def add_survey(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None)
):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": True,
                    "message": "Only PDF files are accepted"
                }
            )

        document_id = str(uuid4())
        file_content = await file.read()  # We need to read the file before the request ends
        
        # Add the processing task to background tasks
        background_tasks.add_task(
            survey_service.create_survey,
            file_content=file_content,
            document_id=document_id,
            description=description,
            title=title or file.filename,
            file_name=file.filename
        )

        return {
            "message": "Survey processing started",
            "document_id": document_id,
            "status": "pending"
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