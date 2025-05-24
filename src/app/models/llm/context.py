


from typing import Literal, Optional, TypedDict


class LLMContext(TypedDict):
    """
    Represents a context for a Large Language Model (LLM) request.
    """
    type: Literal["text", "file"]
    id: str
    context: str
    label: Optional[str] = None
    urls: Optional[list[str]] = None
   
