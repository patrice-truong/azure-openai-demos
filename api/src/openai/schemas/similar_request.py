from typing import List
from pydantic import BaseModel

class SimilarRequest(BaseModel):
    queryVector: List[float]
    limit: int = 5
    min_score: float = 0.8
