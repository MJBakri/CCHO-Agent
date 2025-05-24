


from typing import Literal
from pydantic import BaseModel


class SocketLLMResponse(BaseModel):
    status: Literal["success", "error", "pending", "thinking"]
    message: str