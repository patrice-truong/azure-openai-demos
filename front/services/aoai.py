import json
from dotenv import load_dotenv

from services.data import post_data
load_dotenv()


# def get_embeddings(url, payload):
#     embeddings = post_data(url, payload)
#     return embeddings

def generate_embeddings(products):
    return post_data("/openai/v1/generate_embeddings", json.dumps(products))

def generate_embeddings_from_text(text):
    payload = {
        "text": text
    }
    return post_data("/openai/v1/generate_embeddings_from_text", json.dumps(payload))