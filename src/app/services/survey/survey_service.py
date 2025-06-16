
from datetime import datetime
from typing import Optional
from pdf2image import convert_from_bytes
from services.llm.llm_service_factory import LLMServiceFactory
from utils.json_converter import dict_bson_to_json
from utils.page import convert_pdf_to_base64_images
from services.db.mongo import MongoDB
from logger.logger import logger
from fastapi import Request, UploadFile
from pymongo.errors import CollectionInvalid
class SurveyService:
    @classmethod
    async def create(cls, mongo: MongoDB):
        # Create instance

        try:
            await mongo.db.create_collection("surveys", ignore_existing=True)
            await mongo.get_database().surveys.create_index("document_id", unique=True)
        except CollectionInvalid as e:
            logger.info(f"Collection 'surveys' already exists")
        return cls(mongo)
        
        
    def __init__(self, mongo: MongoDB = None):
        self.mongo = mongo
        logger.debug("SurveyService initialized")
        
    async def get_survey(self, document_id:str) -> dict:
        return await self.mongo.get_database().get_collection("surveys").find_one({"document_id": document_id})
        
    async def get_surveys(self, filters: dict = {}):
        if filters is None:
            filters = {}
        
        result = self.mongo.get_database().get_collection("surveys").find(filters)
        return result
    
    async def create_survey(self, file_content:bytes, document_id:str, description:Optional[str]=None, title:Optional[str]=None, file_name:Optional[str] = None):
        # Convert PDF pages to images
        
        
        images = convert_pdf_to_base64_images(pdf_content=file_content)

        survey_data = {
            "title": title if title else file_name,
            "description": description or "",
            "file_name":file_name,
            "document_id": document_id,
            "status": "pending",
            "uploaded_on": int(datetime.now().timestamp() * 1000),
            "processed_finished" : None,
            # "file_content": pdf_content,
            "pages": len(images),
            "content": {}
        }
        await self.mongo.get_database().surveys.insert_one(dict_bson_to_json(survey_data))
        
        vision_model = LLMServiceFactory.create_llm(
            "groq",
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            prompt="""You are going to receive a page of a medical survey, and you will convert it to a markdown. Keep in mind the type of question and make sure that it is understandable and complete when you convert it to markdown. You don't need to copy the exactly the format but you can convert the survey into a more readable friendly way. For example, if you see questions in a table and the choices are in the top column, you may convert this type of questions into simple multiple choice type of questions. Or let's say for example the choices are needed to be encircled. You can convert this to multiple choices as well. Only output the markdown without any other text.""",
        )
        
        doc_content = ""
        for i in range(0, len(images), 3):
            # Get up to 3 images at a time
            batch = images[i:i+3]
            attachments = [
                {
                    "type": "image",
                    "data": img["image"]
                } for img in batch
            ]
            
            content = await vision_model.send_to_llm(attachments=attachments)
            doc_content += f"{content}\n"

        survey_data["content"]["whole_document"] = doc_content.strip()
        
        await self.mongo.get_database().surveys.update_one({"document_id": document_id}, {"$set": {
                "content": survey_data["content"],
                "status": "done",
                "processed_finished": int(datetime.now().timestamp() * 1000),
            }})
        
        
        
        
        return survey_data

        # Save to database
        # result = await survey_service.create_survey(survey_data)

