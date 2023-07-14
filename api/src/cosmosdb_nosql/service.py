from datetime import datetime
from typing import List
import uuid
from azure.cosmos import CosmosClient, PartitionKey

from src.openai.schemas.completion import CompletionRequest
from src.openai.schemas.summary import SummaryRequest

from .models.chat_message import ChatMessage
from .models.chat_session import ChatSession
from src.openai.service import OpenAIService

import os

class CosmosDBService:
    def __init__(self):
        endpoint = os.environ.get("COSMOSDB_ENDPOINT")
        key = os.environ.get("COSMOSDB_KEY")
        database_name = os.environ.get("COSMOSDB_DATABASE_NAME")
        container_name = os.environ.get("COSMOSDB_CONTAINER_NAME")

        self.client = CosmosClient(endpoint, key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    # check if the Cosmos DB service is running OK
    def check_server_status(self):
        try:
            items = self.container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            )
            return "Cosmos DB service is running OK"
        except Exception as e:
            return f"Cosmos DB service error: {str(e)}"

    # get all chat history    
    def get_chat_history(self) -> List[ChatSession]:
        items = self.container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )
        return [item for item in items]

    # create a new chat session   
    def create_chat_session(self, chat_session: ChatSession) -> ChatSession:
        self.container.create_item(body=chat_session, partition_key=chat_session["ChatSessionId"])
        return chat_session

    # get chat history by chatSessionId
    def get_chat_history_by_session_id(self, session_id: str) -> ChatSession:
        query = f"SELECT * FROM c WHERE c.ChatSessionId = '{session_id}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        # chat_history = ChatSession(**items[0]) if items else None
        chat_history = items[0] if items else None
        return chat_history
    
    # get chat history by user email
    def get_chat_history_by_user_email(self, user_email: str) -> List[ChatSession]:
        query = f"SELECT * FROM c WHERE c.UserEmail = '{user_email}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        chat_history = [item for item in items]
        return chat_history
        
    # delete a chat session by chatSessionId and all associated chat messages
    def delete_chat_history_by_session_id(self, session_id: str):
        query = f"SELECT * FROM c WHERE c.ChatSessionId = '{session_id}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        for item in items:
            id = item["id"]
            partitionKey = item["ChatSessionId"]
            self.container.delete_item(id, partitionKey)

        return {"message": "Chat session deleted successfully"}
    
    # Delete all chat history, except sessions with "ChatSessionId" IN ("b0a08b4e-3edf-44c3-a50c-fe2cab3a4ba3", "84924ac7-390d-4939-9be8-48ce980b13b0","13831ade-2086-485d-b2dc-e7796012dbc8")
    def cleanup(self):
        query = f"SELECT * FROM c WHERE c.ChatSessionId NOT IN ('b0a08b4e-3edf-44c3-a50c-fe2cab3a4ba3', '84924ac7-390d-4939-9be8-48ce980b13b0','13831ade-2086-485d-b2dc-e7796012dbc8')"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        for item in items:
            id = item["id"]
            partitionKey = item["ChatSessionId"]
            self.container.delete_item(id, partitionKey)

        return {"message": "Cleanup successful"}
    
    def create_chat_message(self, chat_message: ChatMessage, openai_service) -> ChatSession:
        # Check if the chat session exists
        if chat_message.ChatSessionId == "":
            # Create a new chat session
            chat_session_id = str(uuid.uuid4())
            chat_session = {
                'id': chat_session_id,
                'ChatSessionId': chat_session_id,
                'Name': '',
                'UserEmail': chat_message.UserEmail,
                'UserName': chat_message.UserName,
                'Type': 'ChatSession',
                'ChatHistory': [],
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Save the new chat session
            chat_session = dict(self.create_chat_session(chat_session))
        else:
            chat_session = dict(self.get_chat_history_by_session_id(chat_message.ChatSessionId))

        # Create history from previous messages
        chat_history = ""
        if len(chat_session["ChatHistory"])>0:
            chat_history = '\n'.join(msg["Text"] for msg in chat_session["ChatHistory"])

        # Call OpenAI completion service
        if chat_message.Text != "":
            completion_request = CompletionRequest(
                context = chat_history,
                question = chat_message.Text
            )
            completion_response = openai_service.generate_completion(completion_request)
            
            # if there is no name for the chat, summarize the question and use that as the name
            if chat_session["Name"] == "":
                summary_request = SummaryRequest(text = completion_response)
                summary = openai_service.generate_summary(summary_request)
                chat_session["Name"] = summary.replace("\n", "")

            # create both user and bot chat messages
            userChatMessage: ChatMessage = {
                'id': chat_session["id"],
                'ChatSessionId': chat_session["id"],
                'UserEmail': chat_message.UserEmail,
                'UserName': chat_message.UserName,
                'Type': 'ChatMessage',
                'Sender': 'user',
                'Text': chat_message.Text,
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            botChatMessage: ChatMessage = {
                'id': chat_session["id"],
                'ChatSessionId': chat_session["id"],
                'UserEmail': "",
                'UserName': "AI Bot",
                'Type': 'ChatMessage',
                'Sender': 'bot',
                'Text': completion_response,
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # append chat messages to chat session
            chat_session["ChatHistory"].append(userChatMessage)
            chat_session["ChatHistory"].append(botChatMessage)
            
            # update chat session
            self.container.upsert_item(body=chat_session)
        return chat_session