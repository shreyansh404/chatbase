#Third party imports
from dotenv import load_dotenv
import os
import re
import uuid
from typing import Optional, Dict
from fastapi import HTTPException, status
from service.intent.intent_identifier import detect_intent

#Local imports
from log import get_logger
from models.chat_base_model import GLPIWebhookPayload, ChatResponse

logger = get_logger()

# Load env from default .env and project .env
load_dotenv()  # default .env in cwd, if present
try:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # chatbase/
    load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
except Exception:
    pass

class ChatBaseProcessor:

    def __init__(self, webhook_payload: GLPIWebhookPayload):
        self.payload = webhook_payload
        self.user_name = (
            getattr(webhook_payload.user, "name", "User")
            if webhook_payload and getattr(webhook_payload, "user", None)
            else "User"
        )
        fields = getattr(webhook_payload, "fields", None) if webhook_payload else None
        self.query = getattr(fields, "content", "") if fields else ""
        self.priority = getattr(fields, "priority", None) if fields else None
        self.email_id = (
            getattr(webhook_payload.user, "email", None)
            if webhook_payload and getattr(webhook_payload, "user", None)
            else None
        )
        self.user_id = (
            getattr(webhook_payload.user, "id", None)
            if webhook_payload and getattr(webhook_payload, "user", None)
            else None
        )
        # GLPI payload carries date at the root level
        self.date = getattr(webhook_payload, "date", None)

    async def process(self) -> ChatResponse:
        try:
            intent = detect_intent(self.query)

            logger.info(f"Detected intent={intent} for user_id={self.user_id}")
            return ChatResponse(reply=intent, action="help")
        except Exception as e:
            logger.exception("Failed to process chat")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process webhook {str(e)}",
            )

    @staticmethod
    def book_service(
        service_type: Optional[str] = None,
        date: Optional[str] = None,
        time: Optional[str] = None,
        apartment_unit: Optional[str] = None,
        contact_name: Optional[str] = None,
        phone: Optional[str] = None,
        problem_summary: Optional[str] = None,
    ) -> Dict[str, Optional[str]]:
        """
        Tool: Book a service request. Returns a booking_id and confirmation message.
        """
        booking_id = f"BK-{str(uuid.uuid4())[:8].upper()}"
        confirmation = f"Booking confirmed for {service_type or 'service'}"
        return {
            "booking_id": booking_id,
            "confirmation": confirmation,
            "service_type": service_type,
            "date": date,
            "time": time,
            "apartment_unit": apartment_unit,
            "contact_name": contact_name,
            "phone": phone,
            "problem_summary": problem_summary,
        }

    @staticmethod
    def check_status(booking_id: str) -> Dict[str, Optional[str]]:
        """
        Tool: Check booking status. Returns current status stub.
        """
        status_map = ["created", "assigned", "en_route", "completed", "cancelled"]
        idx = sum(ord(c) for c in booking_id) % len(status_map) if booking_id else 0
        eta = "Today, 6:00 PM" if status_map[idx] in ("assigned", "en_route") else None
        return {"booking_id": booking_id, "status": status_map[idx], "eta": eta}