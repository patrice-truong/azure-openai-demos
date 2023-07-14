from datetime import datetime
from typing import List
from urllib.parse import quote_plus
from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse

from config import Settings


import os

from .schemas.product import Product

class CosmosDB_MongoDB_Service:
    def __init__(self, collection):
        self.collection = collection

    # check if the Cosmos DB service is running OK
    async def service_check(self):
        try:
            products = []
            async for product in self.collection.find().limit(1):
                serialized_product = {**product, "_id": str(product["_id"])}
                products.append(serialized_product)

            return "Cosmos DB for MongoDB service is running OK"
        except Exception as e:
            return f"Cosmos DB for MongoDB service error: {str(e)}"

    # get all products
    async def get_products(self, limit: int = 10):
        products = []
        async for product in self.collection.find().limit(limit):
            serialized_product = {**product, "_id": str(product["_id"])}
            products.append(serialized_product)
        return JSONResponse(content=products)
    
    # count products
    async def count_products(self):
        return await self.collection.count_documents({})

    # insert one product
    async def insert_one(self, product: Product):
        result = await self.collection.insert_one(dict(product))
        return JSONResponse(content={"inserted_id": str(result.inserted_id)})

    # Insert many products
    async def insert_many(self, products: List[Product]):
        # Create a list of product documents
        product_documents = []
        for product in products:
            product_documents.append(product.dict())
        # Insert many documents
        response = await self.collection.insert_many(product_documents)
        return {'message': f'{len(products)} documents successfully created'}

    # Get a product by id
    async def get_product_by_id(self, id: str):
        product = await self.collection.find_one({'_id': ObjectId(id)})
        if product:
            serialized_product = {**product, "_id": str(product["_id"])}
            return JSONResponse(content=serialized_product)
        else:
            raise HTTPException(status_code=404, detail='Product not found')
        
    # Update a product by id
    async def update_product_by_id(self, id: str, product: Product):
        # Return a 404 if the product doesn't exist.
        if await self.collection.find_one({'_id': ObjectId(id)}) is None:
            raise HTTPException(status_code=404, detail='Product not found')
        # Update the product.
        await self.collection.update_one({'_id': ObjectId(id)}, {'$set': product.dict()})
        return {'message': 'Product successfully updated'}
    
    # Delete a product by id
    async def delete_product_by_id(self, id: str):
        # Return a 404 if the product doesn't exist.
        if await self.collection.find_one({'_id': ObjectId(id)}) is None:
            raise HTTPException(status_code=404, detail='Product not found')
        # Delete the product.
        await self.collection.delete_one({'_id': ObjectId(id)})
        return {'message': 'Product successfully deleted'}
    
    # Cleanup all products
    async def cleanup(self):
        async for product in self.collection.find():
            serialized_product = {**product, "_id": str(product["_id"])}
            await self.collection.delete_one({'_id': ObjectId(serialized_product["_id"])})  
        return {'message': 'Cleanup successful'}
    
    async def similar(self, queryVector, limit, min_score):
        pipeline = [
            {
                '$search': {
                    'cosmosSearch': {
                        'vector': queryVector,
                        'path': 'vectorContent',
                        'k': limit
                    },
                    'returnStoredSource': True
                }
            }
        ]

        products = []
        async for product in self.collection.aggregate(pipeline):
            serialized_product = {**product, "_id": str(product["_id"])}
            products.append(serialized_product)

        return JSONResponse(content=products)
            
