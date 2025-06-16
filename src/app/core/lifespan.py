from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.db.mongo import MongoDB
from logger.logger import logger
import os
from dotenv import load_dotenv
load_dotenv()
from core.dependencies import mongo_client, survey_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialized services.")   
    
    yield
      
    logger.info("Shutting down services...")
    await mongo_client.close()
    
    logger.info("Services shutdown completed")

