from typing import List
from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embeddings: List[float]