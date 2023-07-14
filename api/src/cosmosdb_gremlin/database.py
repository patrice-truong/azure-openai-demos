from gremlin_python.driver import client, serializer

import config

settings = config.get_current_server_config()

COSMOSDB_GREMLIN_ENDPOINT = settings.COSMOSDB_GREMLIN_ENDPOINT
COSMOSDB_GREMLIN_KEY = settings.COSMOSDB_GREMLIN_KEY
COSMOSDB_GREMLIN_DATABASE_NAME = settings.COSMOSDB_GREMLIN_DATABASE_NAME
COSMOSDB_GREMLIN_COLLECTION__NAME = settings.COSMOSDB_GREMLIN_COLLECTION__NAME

def get_client():
    gremlin_client = client.Client(
                        COSMOSDB_GREMLIN_ENDPOINT, 
                        'g',
                        username=f"/dbs/{COSMOSDB_GREMLIN_DATABASE_NAME}/colls/{COSMOSDB_GREMLIN_COLLECTION__NAME}",
                        password=COSMOSDB_GREMLIN_KEY,
                        message_serializer=serializer.GraphSONSerializersV2d0()
                    )
    try:
        yield gremlin_client
    finally:
        pass