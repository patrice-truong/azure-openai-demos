from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from config import Settings

settings = config.get_current_server_config()

SQL_DATABASE_URL = settings.SQL_DATABASE_URL

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    """
    This method is used to create the database instance.
    :return: database instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()