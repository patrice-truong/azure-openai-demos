from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from src.openai.schemas.completion import CompletionRequest
from .models.chat_message import ChatMessage
from src.openai.service import OpenAIService
from .schemas.chat_session import ChatSession
from .models.chat_session import ChatSession
from .schemas.chat_message import ChatMessageCreate
from .service import CosmosDBService
from typing import List, Optional

router = APIRouter()

@router.get("/v1/server-check")
def server_check(service: CosmosDBService = Depends()):
    service_status = service.check_server_status()
    return {"message": service_status}

@router.get("/v1/chat", response_model=List[ChatSession])
def get_chat_history(service: CosmosDBService = Depends()):
    return service.get_chat_history()

@router.get("/v1/chat/{session_id}", response_model=ChatSession)
def get_chat_history_by_session_id(session_id: str, service: CosmosDBService = Depends()):
    return service.get_chat_history_by_session_id(session_id)

@router.get("/v1/chat/user/{user_email}", response_model=List[ChatSession])
def get_chat_history_by_user_email(user_email: str, service: CosmosDBService = Depends()):
    return service.get_chat_history_by_user_email(user_email)

# create a chat message
# if the chat session exists, add the chat message to the chat history
# if the chat session does not exist, create a new chat session and add the chat message to the chat history
# call OpenAI completion API
# process the completion response and update chat history if needed

@router.post("/v1/chat", response_model=ChatSession)
def create_chat_message(chat_message: ChatMessageCreate,
                        service: CosmosDBService = Depends(),
                        openai_service: OpenAIService = Depends()):
    return service.create_chat_message(chat_message, openai_service)
    
@router.delete("/v1/chat/{session_id}")
def delete_chat_history_by_session_id(session_id: str, service: CosmosDBService = Depends()):
    return service.delete_chat_history_by_session_id(session_id)

# Delete all chat history, except sessions with "ChatSessionId" IN ("b0a08b4e-3edf-44c3-a50c-fe2cab3a4ba3", "84924ac7-390d-4939-9be8-48ce980b13b0","13831ade-2086-485d-b2dc-e7796012dbc8")

@router.post("/v1/chat/cleanup")
def cleanup(service: CosmosDBService = Depends()):
    return service.cleanup()