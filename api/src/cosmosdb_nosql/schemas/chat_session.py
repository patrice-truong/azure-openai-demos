from typing import List, Optional
from pydantic import BaseModel

from src.cosmosdb_nosql.models.chat_message import ChatMessage

class ChatSession(BaseModel):
    id: Optional[str]
    ChatSessionId: str
    Type: str
    Name: Optional[str]
    UserEmail: str
    UserName: str
    ChatHistory: List[ChatMessage]
    Timestamp: str
