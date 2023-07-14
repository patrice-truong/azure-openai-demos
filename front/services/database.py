from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

SQL_SERVER_ENDPOINT=os.getenv("SQL_SERVER_ENDPOINT")
SQL_SERVER_DATABASE=os.getenv("SQL_SERVER_DATABASE")
SQL_SERVER_USERNAME=os.getenv("SQL_SERVER_USERNAME")
SQL_SERVER_PASSWORD=os.getenv("SQL_SERVER_PASSWORD")

# SQL Server
DATABASE_URL = "mssql+pymssql://" + SQL_SERVER_USERNAME + ":" + SQL_SERVER_PASSWORD + "@" + SQL_SERVER_ENDPOINT + "/" + SQL_SERVER_DATABASE

engine = create_engine(
    DATABASE_URL, connect_args={"autocommit": True}
)

