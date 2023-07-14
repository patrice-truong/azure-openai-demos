from sqlalchemy import Column, Integer, String, Float, DateTime
from logging.config import dictConfig
import logging
from sqlalchemy import Column
from config import LogConfig
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

dictConfig(LogConfig().dict())
logger = logging.getLogger("fastapi-project")

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(length=100))
    artist = Column(String(length=100))
    duration = Column(Float)
    last_play = Column(DateTime)
