"""
Class-based FastApi app Configuration.
config class is for base configuration.
"""
import os

from datetime import timedelta
from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic import BaseModel
from logging.config import dictConfig
import logging

SERVER_TYPE_PRODUCTION = "production"
SERVER_TYPE_DEVELOPMENT = "development"

load_dotenv()

class Settings(BaseSettings):
    # https://pydantic-docs.helpmanual.io/usage/settings/
    SQL_DATABASE_URL: str = os.getenv("SQL_DATABASE_URL")
    
    COSMOSDB_ENDPOINT: str = os.getenv("COSMOSDB_ENDPOINT")
    COSMOSDB_KEY: str = os.getenv("COSMOSDB_KEY")
    COSMOSDB_DATABASE_NAME: str = os.getenv("COSMOSDB_DATABASE_NAME")
    COSMOSDB_CONTAINER_NAME: str = os.getenv("COSMOSDB_CONTAINER_NAME")
    
    COSMOSDB_GREMLIN_ENDPOINT: str = os.getenv("COSMOSDB_GREMLIN_ENDPOINT")
    COSMOSDB_GREMLIN_KEY: str = os.getenv("COSMOSDB_GREMLIN_KEY")
    COSMOSDB_GREMLIN_DATABASE_NAME: str = os.getenv("COSMOSDB_GREMLIN_DATABASE_NAME")
    COSMOSDB_GREMLIN_COLLECTION__NAME: str = os.getenv("COSMOSDB_GREMLIN_COLLECTION__NAME")

    COSMOSDB_MONGODB_HOST: str = os.getenv("COSMOSDB_MONGODB_HOST")
    COSMOSDB_MONGODB_USERNAME: str = os.getenv("COSMOSDB_MONGODB_USERNAME")
    COSMOSDB_MONGODB_PASSWORD: str = os.getenv("COSMOSDB_MONGODB_PASSWORD")
    COSMOSDB_MONGODB_DATABASE: str = os.getenv("COSMOSDB_MONGODB_DATABASE")
    COSMOSDB_MONGODB_COLLECTION: str = os.getenv("COSMOSDB_MONGODB_COLLECTION")
    COSMOSDB_MONGODB_PORT: str = os.getenv("COSMOSDB_MONGODB_PORT")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PATOCHE_OPENAI_API_KEY: str = os.getenv("PATOCHE_OPENAI_API_KEY")
    OPENAI_ENDPOINT: str = os.getenv("OPENAI_ENDPOINT")
    OPENAI_APITYPE: str = os.getenv("OPENAI_APITYPE")
    MAX_TOKENS: str = os.getenv("MAX_TOKENS")
    TEMPERATURE: str = os.getenv("TEMPERATURE")
    MODEL_ENGINE: str = os.getenv("MODEL_ENGINE")

    # JWT Token configuration
    # JWT_TOKEN_EXPIRES: timedelta = timedelta(hours=48)
    # JWT_ALGORITHM: str = "HS384"
    # authjwt_header_type: str = "Bearer"
    # authjwt_secret_key: str
    # # Configure algorithms which is permit
    # authjwt_decode_algorithms: set = {"HS384", "HS512"}

    # # Domain
    # LOCAL_HOST_URL: str

    # database settings.
    AUTOCOMMIT: bool = True
    AUTOFLUSH: bool = True

    class Config:
        env_file = '.env'  # set the env file path.
        env_file_encoding = 'utf-8'


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    # https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api

    LOGGER_NAME: str = "fastapi-project"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "fastapi-project": {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("fastapi-project")


def get_current_server_config():
    """
    This will check FastApi_ENV variable and create an object of configuration according to that 
    :return: Production or Development Config object.
    """
    current_config = os.getenv("ENV_FASTAPI_SERVER_TYPE", SERVER_TYPE_DEVELOPMENT)
    return DevelopmentConfig() if current_config == SERVER_TYPE_DEVELOPMENT else ProductionConfig()


class Config(object):
    """
    Set base configuration, env variable configuration and server configuration.
    """
    # The starting execution point of the app.
    FASTAPI_APP = 'main.py'


class DevelopmentConfig(Config):
    """
        This class for generates the config for development instance.
        """
    DEBUG: bool = True
    TESTING: bool = True
    
    SQL_DATABASE_URL = Settings().SQL_DATABASE_URL

    COSMOSDB_ENDPOINT = Settings().COSMOSDB_ENDPOINT
    COSMOSDB_KEY = Settings().COSMOSDB_KEY
    COSMOSDB_DATABASE_NAME = Settings().COSMOSDB_DATABASE_NAME
    COSMOSDB_CONTAINER_NAME = Settings().COSMOSDB_CONTAINER_NAME
    
    COSMOSDB_GREMLIN_ENDPOINT = Settings().COSMOSDB_GREMLIN_ENDPOINT
    COSMOSDB_GREMLIN_KEY = Settings().COSMOSDB_GREMLIN_KEY
    COSMOSDB_GREMLIN_DATABASE_NAME = Settings().COSMOSDB_GREMLIN_DATABASE_NAME
    COSMOSDB_GREMLIN_COLLECTION__NAME = Settings().COSMOSDB_GREMLIN_COLLECTION__NAME

    OPENAI_API_KEY = Settings().OPENAI_API_KEY
    PATOCHE_OPENAI_API_KEY = Settings().PATOCHE_OPENAI_API_KEY
    OPENAI_ENDPOINT = Settings().OPENAI_ENDPOINT
    OPENAI_APITYPE = Settings().OPENAI_APITYPE
    MAX_TOKENS = Settings().MAX_TOKENS
    TEMPERATURE = Settings().TEMPERATURE
    MODEL_ENGINE = Settings().MODEL_ENGINE

    COSMOSDB_MONGODB_HOST = Settings().COSMOSDB_MONGODB_HOST
    COSMOSDB_MONGODB_USERNAME = Settings().COSMOSDB_MONGODB_USERNAME
    COSMOSDB_MONGODB_PASSWORD = Settings().COSMOSDB_MONGODB_PASSWORD
    COSMOSDB_MONGODB_DATABASE = Settings().COSMOSDB_MONGODB_DATABASE
    COSMOSDB_MONGODB_COLLECTION = Settings().COSMOSDB_MONGODB_COLLECTION
    COSMOSDB_MONGODB_PORT = Settings().COSMOSDB_MONGODB_PORT

class ProductionConfig(Config):
    """
    This class for generates the config for the development instance.
    """
    DEBUG: bool = False
    TESTING: bool = False
