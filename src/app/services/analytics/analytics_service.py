
from datetime import datetime
from typing import Optional
from pdf2image import convert_from_bytes
from services.llm.llm_service_factory import LLMServiceFactory
from utils.json_converter import dict_bson_to_json
from utils.page import convert_pdf_to_base64_images
from services.db.mongo import MongoDB
from logger.logger import logger
from fastapi import Request, UploadFile
import pandas as pd
from pymongo.errors import CollectionInvalid
from io import BytesIO
class AnalyticsService:
    @classmethod
    async def create(cls, mongo: MongoDB):
        # Create instance

        try:
            await mongo.db.create_collection("analytics", ignore_existing=True)
            await mongo.get_database().analytics.create_index("document_id", unique=True)
        except CollectionInvalid as e:
            logger.info(f"Collection 'analytics' already exists")
        return cls(mongo)
        
        
    def __init__(self, mongo: MongoDB = None):
        self.mongo = mongo
        logger.debug("AnalyticsService initialized")
        
    async def get_analytics(self, document_id:str) -> dict:
        return await self.mongo.get_database().get_collection("analytics").find_one({"document_id": document_id})
        
    async def get_analytics_collection(self, filters: dict = {}):
        if filters is None:
            filters = {}
        
        result = self.mongo.get_database().get_collection("analytics").find(filters)
        return result
    
    async def create_analytics(self, file_content:bytes, document_id:str, description:Optional[str]=None, title:Optional[str]=None, file_name:Optional[str] = None):
        # Convert PDF pages to images
        
        df = pd.read_excel(BytesIO(file_content))
        # data_dict = df.to_markdown()
        
        def df_to_minimal_markdown(df):
            header = '|'.join(df.columns)
            separator = '|'.join(['---'] * len(df.columns))
            rows = ['|'.join(map(str, row)) for row in df.values.tolist()]
            return '\n'.join([f'|{header}|', f'|{separator}|'] + [f'|{row}|' for row in rows])


        analytics_data = {
            "title": title if title else file_name,
            "description": description or "",
            "file_name":file_name,
            "document_id": document_id,
            "uploaded_on": int(datetime.now().timestamp() * 1000),
            "content": {
                "whole": df_to_minimal_markdown(df)
            }
        }
        await self.mongo.get_database().analytics.insert_one(dict_bson_to_json(analytics_data))
        
    
        
        
        return analytics_data


