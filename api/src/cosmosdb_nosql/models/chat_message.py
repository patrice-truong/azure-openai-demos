from pydantic import BaseModel

class ChatMessage(BaseModel):
    id: str
    ChatSessionId: str
    UserEmail: str
    UserName: str
    Type: str
    Sender: str
    Text: str
    Timestamp: str
