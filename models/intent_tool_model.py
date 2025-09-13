from pydantic import BaseModel
from typing import Literal, Optional
from google.generativeai.agent import Tool, tool_fn

class IntentRequest(BaseModel):
    text: str

class IntentResult(BaseModel):
    intent: Literal["book_service", "status_check", "cancel_booking", "reschedule_booking", "pricing", "help", "other"]
    service_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    apartment_unit: Optional[str] = None

@tool_fn
def extract_intent(req: IntentRequest) -> IntentResult:
    """
    Extracts structured intent from user text.
    """
    if "plumber" in req.text.lower():
        return IntentResult(intent="book_service", service_type="plumber")
    return IntentResult(intent="other")