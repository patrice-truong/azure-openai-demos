from pydantic import BaseModel
from datetime import datetime

class TrackBase(BaseModel):
    title: str
    artist: str
    duration: float
    last_play: datetime

class TrackCreate(TrackBase):
    pass

class TrackUpdate(TrackBase):
    pass

class TrackInDB(TrackBase):
    id: int

    class Config:
        orm_mode = True
