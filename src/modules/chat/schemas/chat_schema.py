from pydantic import BaseModel

class CHAT_schema(BaseModel): 
    promt: str
    difficulty: str