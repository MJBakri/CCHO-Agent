from services.survey.survey_service import SurveyService
from services.analytics.analytics_service import AnalyticsService
from services.db.mongo import MongoDB
import os
from dotenv import load_dotenv
load_dotenv()

mongo_client = MongoDB(
    uri=os.getenv("MONGO_URI", ""),
    db_name=os.getenv("MONGO_DB_NAME", "")
)

survey_service = SurveyService(mongo=mongo_client)
analytics_service = AnalyticsService(mongo=mongo_client)
