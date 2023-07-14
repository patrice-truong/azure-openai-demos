from typing import List, Optional
from pydantic import BaseModel

from src.cosmosdb_nosql.models.chat_message import ChatMessage

class ChatMessage(BaseModel):
    id: str
    ChatSessionId: Optional[str]
    UserEmail: str
    UserName: str
    Type: str = 'ChatMessage'
    Sender: str = 'user'
    Text: str
    Timestamp: Optional[str]

class ChatMessageCreate(BaseModel):
    ChatSessionId: Optional[str]
    UserEmail: str
    UserName: str
    Text: str
