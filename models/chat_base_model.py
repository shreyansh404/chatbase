from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import time

class GLPIUser(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

class GLPIEventFields(BaseModel):
    name: str
    content: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[int] = None
    entities_id: Optional[int] = None

class GLPIWebhookPayload(BaseModel):
    event: str                 # e.g. "message", "ticket.create"
    itemtype: str              # e.g. "Ticket"
    items_id: int
    date: str = time.time()
    user: GLPIUser
    fields: GLPIEventFields


class ChatResponse(BaseModel):
    success: bool = True
    reply: list = []
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None