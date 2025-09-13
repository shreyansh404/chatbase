from typing import Optional, Dict, Any
from pydantic import BaseModel


class GLPIUser(BaseModel):
    id: int
    name: str
    email: Optional[str]


class GLPIEventFields(BaseModel):
    name: str
    content: Optional[str]
    priority: Optional[int]
    status: Optional[int]
    entities_id: Optional[int]


class GLPIWebhookPayload(BaseModel):
    event: str
    itemtype: str
    items_id: int
    date: str
    user: GLPIUser
    fields: GLPIEventFields


class ChatResponse(BaseModel):
    success: bool = True
    reply: str
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None