from datetime import datetime
from fastapi import APIRouter, Depends

from .schemas.query import Query
from .database import get_client
from .service import CosmosDBforGremlinService
from typing import List, Optional

router = APIRouter()

@router.get("/v1/service_check")
def service_check(client = Depends(get_client)):
    service = CosmosDBforGremlinService(client)
    service_status = service.service_check()
    return {"message": service_status}

@router.get("/v1/count")
def service_check(client = Depends(get_client)):
    service = CosmosDBforGremlinService(client)
    count = service.count()    
    return {"message": count}

@router.post("/v1/execute_query")
def execute_query(query: Query, client = Depends(get_client)):
    service = CosmosDBforGremlinService(client)
    result = service.execute_query(query.Text)    
    return {"message": result}