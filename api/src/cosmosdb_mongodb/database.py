from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

import config
from config import Settings

settings = config.get_current_server_config()

COSMOSDB_MONGODB_HOST = settings.COSMOSDB_MONGODB_HOST
COSMOSDB_MONGODB_USERNAME = settings.COSMOSDB_MONGODB_USERNAME
COSMOSDB_MONGODB_PASSWORD = settings.COSMOSDB_MONGODB_PASSWORD
COSMOSDB_MONGODB_DATABASE = settings.COSMOSDB_MONGODB_DATABASE
COSMOSDB_MONGODB_COLLECTION = settings.COSMOSDB_MONGODB_COLLECTION
COSMOSDB_MONGODB_PORT = settings.COSMOSDB_MONGODB_PORT

uri = f'mongodb+srv://{quote_plus(COSMOSDB_MONGODB_USERNAME)}:{quote_plus(COSMOSDB_MONGODB_PASSWORD)}@{COSMOSDB_MONGODB_HOST}/?"tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"'

client = AsyncIOMotorClient(uri, ssl=True)
database = client[COSMOSDB_MONGODB_DATABASE]

def get_collection():
    database = client[COSMOSDB_MONGODB_DATABASE]
    collection = database[COSMOSDB_MONGODB_COLLECTION]
    try:
        yield collection
    finally:
        pass