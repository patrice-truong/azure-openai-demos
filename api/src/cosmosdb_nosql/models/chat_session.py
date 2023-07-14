from typing import List
from pydantic import BaseModel

from src.cosmosdb_nosql.models.chat_message import ChatMessage

class ChatSession(BaseModel):
    id: str
    ChatSessionId: str
    Type: str
    Name: str
    UserEmail: str
    UserName: str
    ChatHistory: List[ChatMessage]
    Timestamp: str
