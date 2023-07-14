from pydantic import BaseModel

class Document(BaseModel):
    name: str
    bio: str
    vectorContent = []