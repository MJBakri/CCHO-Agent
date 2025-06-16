

from typing import Any, Literal, TypedDict


class MessageAttachment(TypedDict):
    type: Literal["text", "image"]
    data: Any