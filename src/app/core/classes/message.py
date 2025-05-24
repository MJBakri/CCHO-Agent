

from typing import List, Literal, Optional, TypedDict
from datetime import datetime
from uuid import uuid4
from logger.logger import logger
from pydantic import BaseModel


class FileReference(TypedDict):
    """A reference to a file that can be attached to a message."""
    id: str
    name: str
    url: str
    size: int
    mime_type: str
    
ChatRole = Literal["user", "assistant", "tool"]

class ChatMessage(BaseModel):
    role: ChatRole
    id:str
    created_at: datetime
    message_versions: list[str] = []
    
    def get_message_age(self) -> float:
        """Return the age of the message in seconds"""
        return (datetime.now() - self.created_at).total_seconds()
    
    def edit_user_message(self, version: str, ) -> None:
        """Add a new version to the versions list"""
        if self.versions is None:
            self.versions = []
        self.versions.append(version)
    
    async def receive_ai_message(self, chars:str):
        if not self.message_versions:
            self.message_versions.append("")
            
        self.message_versions[-1] += chars
            
    def get_latest_message(self) -> str:
        """Return the latest message version"""
        return self.message_versions[-1]
    
    @classmethod
    def create_message(cls, role:ChatRole, message:Optional[str]=None, id:str = uuid4(), message_versions:List[str]=[]) -> "ChatMessage":
        """Create a new user message"""
        
        mv = [*message_versions]
        if message:
            mv.append(message)
        return cls(
            role=role,
            id=str(id),
            created_at=datetime.now(),
            message_versions=mv
        )