from typing import List, Optional
from pydantic import BaseModel

class Query(BaseModel):
    Text: str
