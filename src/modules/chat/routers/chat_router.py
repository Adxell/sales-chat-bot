from fastapi import APIRouter, Depends
from fastapi.requests import Request
from sqlalchemy.orm import Session

from ..queries.chat_queries import create_chat, chat_bot
from db_config.database import get_db
from fastapi import BackgroundTasks
from urllib.parse import parse_qs


router = APIRouter() 


@router.post('/create-chat')
async def post(request: Request, db: Session = Depends(get_db)):
    # Decode and parse request body
    response_body = await request.body()
    parsed_data = parse_qs(response_body.decode("utf-8"))

    # Extract user and level
    user = parsed_data.get("user_name", [""])[0]
    level = parsed_data.get("text", [""])[0].upper()

    # Validate level
    if level not in {"BASICO", "MEDIO", "COMPLEJO"}:
        return "Por favor, elija entre 'Basico', 'Medio' o 'Complejo'."

    # Create chat session
    response_created_chat = create_chat(db, user, level)

    return response_created_chat


@router.post('/chat-bot')
async def post(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Decode request body and parse form data
    response_body = await request.body()
    parsed_data = parse_qs(response_body.decode("utf-8"))

    # Extract user and message
    user = parsed_data.get("user_name", [""])[0]
    message = parsed_data.get("text", [""])[0]

    if not user or not message:
        return "Invalid request: missing user_name or text."

    # Process message asynchronously
    background_tasks.add_task(chat_bot, db, user, message)

    return f"{message.replace('+', ' ')} (Sent)"




