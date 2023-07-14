from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import Request

from src.cosmosdb_mongodb.schemas.product import Product

from .schemas.completion import CompletionRequest
from .schemas.summary import SummaryRequest
from .schemas.embedding_request import EmbeddingRequest, EmbeddingResponse
from .service import OpenAIService

router = APIRouter()

@router.get("/v1/service_check")
def service_check(service: OpenAIService = Depends()):
    return service.service_check()

@router.post("/v1/generate_completion")
def generate_completion(request: CompletionRequest, service: OpenAIService = Depends()):
    completion = service.generate_completion(request)
    return {"result": completion}


@router.post("/v1/generate_summary")
def generate_summary(request: SummaryRequest, service: OpenAIService = Depends()):
    summary = service.generate_summary(request)
    return {"result": summary}

@router.post('/v1/generate_embeddings')
def generate_embeddings(products: List[Product], service: OpenAIService = Depends()):
    embeddings = service.generate_embeddings(products)
    return JSONResponse(content=embeddings)

@router.post('/v1/generate_embeddings_from_text', response_model=EmbeddingResponse)
def generate_embeddings_from_text(request: EmbeddingRequest, service: OpenAIService = Depends()): 
    text = request.text
    embeddings = service.generate_embeddings_from_text(text)
    embeddings_float = [float(embedding) for embedding in embeddings]
    return EmbeddingResponse(embeddings=embeddings_float)

