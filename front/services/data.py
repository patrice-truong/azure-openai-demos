import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_data(url):
    headers = {
        'Content-Type': 'application/json',
    }
    apiEndpoint = os.getenv('API_ENDPOINT')
    url = f"{apiEndpoint}{url}"
    return requests.get(
        url, 
        headers=headers
    )

def post_data(url, payload):
    headers = {
        'Content-Type': 'application/json',
    }
    apiEndpoint = os.getenv('API_ENDPOINT')
    url = f"{apiEndpoint}{url}"

    return requests.post(
        url, 
        headers = headers,
        data = payload
    )

def delete_data(url):
    headers = {
        'Content-Type': 'application/json',
        # 'authorization': 'Bearer ' + token
    }
    apiEndpoint = os.getenv('API_ENDPOINT')
    url = f"{apiEndpoint}{url}"

    return requests.delete(
        url, 
        headers = headers
    )


