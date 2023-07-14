import json
import streamlit as st
from services.data import get_data, post_data


def get_products():
    return get_data("/cosmosdb_mongodb/v1/product").json()

def count_products():
    return get_data("/cosmosdb_mongodb/v1/product/count").json()

def insert_one(product):
    response = post_data("/cosmosdb_mongodb/v1/product/insert_one", product)
    return response

def insert_many(products):
    return post_data("/cosmosdb_mongodb/v1/product/insert_many", json.dumps(products))

def similar(query_vector, limit=5, min_score=0.8):
    payload = { 
        "queryVector": query_vector,
        "limit": limit,
        "min_score": min_score
    }

    return post_data("/cosmosdb_mongodb/v1/product/similar", json.dumps(payload))
    