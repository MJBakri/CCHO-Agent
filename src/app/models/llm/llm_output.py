from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional, TypedDict


class LLMOutput(TypedDict):
    content: str
    model: str
    created_at: datetime = datetime.now()
    usage: Dict[str, int] = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }
    finish_reason: Optional[str] = None
    status: str = "success"
