from pydantic import BaseModel

class ChatResponse(BaseModel):
    role: str
    content: str