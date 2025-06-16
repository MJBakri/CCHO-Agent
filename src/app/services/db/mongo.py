from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from logger.logger import logger
load_dotenv()
import os

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        logger.debug(f"Connected to MongoDB. Database: {db_name}")
        
    def get_client(self):
        return self.client
    
    def get_database(self):
        return self.db

    async def close(self):
        self.client.close()
