from typing import List
import openai
import os

import requests

from src.cosmosdb_mongodb.schemas.product import Product
from .schemas.completion import CompletionRequest
from .schemas.summary import SummaryRequest

class OpenAIService:

    def __init__(self):
        self.model_engine = os.environ.get("MODEL_ENGINE")
        self.max_tokens = int(os.environ.get("MAX_TOKENS"))
        self.temperature = float(os.environ.get("TEMPERATURE"))
        self.patoche_openai_key = os.environ.get("PATOCHE_OPENAI_API_KEY")

    def service_check(self):
        return "OpenAI service is running OK"

    def generate_completion(self, request: CompletionRequest) -> str:
        openai.api_base = os.environ.get("OPENAI_ENDPOINT")
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_version = "2023-05-15"
        openai.api_type = "azure"

        prompt = f"""
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        {request.context}
        Question: {request.question}
        Answer:
        """

        # Send a completion call to generate an answer
        response = openai.Completion.create(
            engine=self.model_engine, 
            prompt=prompt, 
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
        return text


    def generate_summary(self, request: SummaryRequest) -> str:
        text = self.generate_completion(
            CompletionRequest(
                context="Summarize this text in less than 30 caracters: ", 
                question=request.text
            )
        )
        return text
        
        
    # Using OpenAI instead of Azure OpenAI, as we can do embedding batch processing on OpenAI
    # https://beta.openai.com/docs/api-reference/embeddings

    def generate_embeddings(self, products: List[Product]) -> List[float]:
        openai.api_base = "https://api.openai.com/v1/"
        openai.api_key = os.environ.get("PATOCHE_OPENAI_API_KEY")
        openai.api_type = "openai"

        # Convert products to a list of dictionaries
        product_dicts = [product.to_json() for product in products]

        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=product_dicts
        )
        
        embeddings = response["data"][0]["embedding"]
        return embeddings
        

    # Create a function to generate embeddings from text
    # using Azure OpenAI API
    def generate_embeddings_from_text(self, text: str) -> List[float]:
        openai.api_base = os.environ.get("OPENAI_ENDPOINT")
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_version = "2023-05-15"
        openai.api_type = "azure"

        response = openai.Embedding.create(
            engine="text-embedding-ada-002",
            input=text
        )
        
        embeddings = response["data"][0]["embedding"]
        return embeddings
    