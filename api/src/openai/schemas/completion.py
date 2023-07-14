from typing import Optional
from pydantic import BaseModel

class CompletionRequest(BaseModel):
    context: Optional[str]
    question: str