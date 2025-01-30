from typing import LiteralString, List, Dict
from uuid import UUID
import uuid

import google.generativeai as genai
from setup_config import settings
from slack_sdk import WebClient
from sqlalchemy.orm import Session
from ..models.chat_model import CHAT_model, MESSAGES_model


client = WebClient(token=settings.SLACK_SIGNING_SECRET)


def generar_prompt_cliente(difficulty: str) -> str:
    """
    Generates a prompt based on the specified customer difficulty level.

    Args:
        difficulty (str): The complexity level of the customer ("BASICO", "MEDIO", "COMPLEJO").

    Returns:
        str: A descriptive prompt for the chatbot interaction.

    Raises:
        ValueError: If the difficulty level is not recognized.
    """
    levels = {
        "BASIC": (
            "Act as a basic-level client who wants to purchase a product. "
            "This client has minimal technical knowledge and asks simple, general questions. "
            "They are interested in basic features like price, color, availability, and ease of use. "
            "Avoid any technical jargon and keep the conversation simple and approachable."
        ),
        "INTERMEDIATE": (
            "Act as an intermediate-level client who wants to purchase a product. "
            "This client has a basic understanding of the product and asks more specific questions. "
            "They are interested in comparing options, learning about key features like battery life, warranty, and performance. "
            "They may also ask for recommendations based on their budget or needs."
        ),
        "COMPLEX": (
            "Act as an advanced-level client who wants to purchase a product. "
            "This client has in-depth technical knowledge and asks detailed, technical questions. "
            "They are interested in specifications like processor model, RAM type, storage speed, and advanced features. "
            "They may also ask about compatibility, return policies, and comparisons with other high-end products."
        ),
    }

    if difficulty not in levels:
        raise ValueError(f"Difficulty level not recognized: {difficulty}")

    return levels[difficulty]

def get_answer_chat(prompt: str, messages: Dict, difficulty: str) -> str:
    """
    Generates a chatbot response based on the given prompt, message history, and difficulty level.

    Args:
        prompt (str): The user's input message.
        messages (Dict): A dictionary containing chat history with a "parts" key.
        difficulty (str): The difficulty level of the chatbot interaction.

    Returns:
        str: The chatbot's response.
    """
    messages['parts'].insert(0, generar_prompt_cliente(difficulty))

    return answer_model(prompt, messages)

def answer_model(prompt: str, history: List) -> LiteralString:
    """
    Generates a response from the Gemini AI model based on the provided prompt and chat history.

    Args:
        prompt (str): The user's input message.
        history (List): The conversation history to maintain context.

    Returns:
        LiteralString: The AI-generated response.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    chat = model.start_chat(history=history)

    return chat.send_message(prompt).text

def chat_bot(db: Session, username: str, message: str) -> None:
    """
    Handles a chatbot interaction by storing user messages, retrieving chat history, 
    generating a response, saving it, and posting it to a communication channel.

    Args:
        db (Session): Database session for querying and committing data.
        username (str): The username associated with the chat session.
        message (str): The user's message to the chatbot.

    Returns:
        LiteralString: The chatbot's response.
    """
    chat_data = db.query(CHAT_model).filter(CHAT_model.username == username).first()
    if not chat_data:
        raise ValueError(f"No chat session found for username: {username}")

    new_message = MESSAGES_model(chat_id=chat_data.id, message=message)
    db.add(new_message)
    db.commit()

    history = db.query(MESSAGES_model.message).filter(MESSAGES_model.chat_id == chat_data.id).all()
    history = [i[0] for i in history] if len(history) > 1 else []
    history.append(message.replace("+", " "))  # Format the message properly

    messages = {'role': 'user', 'parts': history}

    answer = get_answer_chat(message, messages, chat_data.level)

    new_message = MESSAGES_model(chat_id=chat_data.id, message=answer)
    db.add(new_message)
    db.commit()

    client.chat_postMessage(
        channel="bot-updates",
        text=answer,
        username="Bot User"
    )

def create_chat(db: Session, username: str, level: str = "Basico") -> LiteralString:
    """
    Creates a new chat session for a user, removing any existing session.

    Args:
        db (Session): The database session for querying and committing data.
        username (str): The username for whom the chat session is created.
        level (str, optional): The difficulty level of the chat. Defaults to "Basico".

    Returns:
        LiteralString: A confirmation message indicating the chat session has been created.
    """
    chat_used = db.query(CHAT_model).filter(CHAT_model.username == username)

    if chat_used.first():
        chat_used.delete()
        db.commit() 

    new_chat = CHAT_model(level=level, username=username)
    db.add(new_chat)
    db.commit()

    return f"Bot created with level {level}"