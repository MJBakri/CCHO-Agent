from typing import Optional
from pydantic import BaseModel


class LLMRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.7
    top_p: int = 1
    top_n: int = 1
    max_tokens: Optional[int] = 2000