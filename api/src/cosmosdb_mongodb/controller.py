from datetime import datetime
from fastapi import APIRouter, Depends, Request

from src.openai.schemas.similar_request import SimilarRequest

from .schemas.product import Product

from .database import get_collection
from .service import CosmosDB_MongoDB_Service
from typing import List, Optional

router = APIRouter()

@router.get("/v1/service_check")
async def server_check(collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    service_status = await service.service_check()
    return {"message": service_status}

# Get all products
@router.get('/v1/product')
async def get_products(collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.get_products()

# count products
@router.get('/v1/product/count')
async def count_products(collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.count_products()

# Insert one product
@router.post('/v1/product/insert_one')
async def insert_one(product: Product, collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.insert_one(product)

# Insert many products
@router.post('/v1/product/insert_many')
async def insert_many(products: List[Product], collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.insert_many(products)

# Read a product by id
@router.get('/v1/product/{id}')
async def get_product_by_id(id: str, collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.get_product_by_id(id)

# Update a product by id
@router.put('/v1/product/{id}')
async def update_product_by_id(id: str, product: Product, collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.update_product_by_id(id, product)

# Delete a product by id
@router.delete('/v1/product/{id}')
async def delete_product_by_id(id: str, collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.delete_product_by_id(id)

# Delete a product by id
@router.delete('/v1/product')
async def cleanup(collection = Depends(get_collection)):
    service = CosmosDB_MongoDB_Service(collection)
    return await service.cleanup()

# Get similar products by comparing vectors
@router.post('/v1/product/similar')
async def similar(similarRequest: SimilarRequest, collection = Depends(get_collection)):
    # payload = { 
    #     "queryVector": queryVector,
    #     "limit": limit,
    #     "min_score": min_score
    # }
    queryVector = similarRequest.queryVector
    limit = similarRequest.limit
    min_score = similarRequest.min_score
    service = CosmosDB_MongoDB_Service(collection)
    return await service.similar(queryVector, limit, min_score)


