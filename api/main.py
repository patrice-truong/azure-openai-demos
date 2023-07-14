from fastapi import FastAPI
from src.cosmosdb_nosql.controller import router as cosmosdb_nosql_router
from src.cosmosdb_mongodb.controller import router as cosmosdb_mongodb_router
from src.cosmosdb_gremlin.controller import router as cosmosdb_gremlin_router
from src.openai.controller import router as openai_router
from src.sqlserver.controller import router as sqlserver_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

app.include_router(cosmosdb_nosql_router, prefix="/cosmosdb_nosql", tags=["Cosmos DB for NoSQL"])
app.include_router(cosmosdb_gremlin_router, prefix="/cosmosdb_gremlin", tags=["Cosmos DB for Gremlin"])
app.include_router(cosmosdb_mongodb_router, prefix="/cosmosdb_mongodb", tags=["Cosmos DB for MongoDB"])
app.include_router(openai_router, prefix="/openai", tags=["OpenAI"])
app.include_router(sqlserver_router, prefix="/sqlserver", tags=["SqlServer"])

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)