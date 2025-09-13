#Third party imports
from dotenv import load_dotenv
import os
import re
import uuid
from typing import Optional, Dict
from fastapi import HTTPException, status

#Local imports
from chatbase.log import get_logger
from chatbase.models.chat_base_model import GLPIWebhookPayload, ChatResponse
from chatbase.models.booking_service import BookServiceRequest, BookServiceResponse

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

    SERVICE_KEYWORDS = {
        "plumber": ["plumber", "plumbing", "nal", "leak", "tap", "geyser", "गीजर", "प्लम्बर"],
        "electrician": ["electric", "fan", "light", "switch", "wiring", "इलेक्ट्रीशियन"],
        "carpenter": ["carpenter", "wood", "door", "hinge", "shelf", "कारपेंटर"],
        "cleaner": ["clean", "deep clean", "सफाई", "क्लीन", "safaai"],
        "pest_control": ["pest", "cockroach", "termite", "bed bug", "कीड़े", "मक्खी"],
        "guard": ["guard", "security", "सिक्योरिटी"],
    }

    def _detect_intent(self, text: str) -> str:
        t = (text or "").lower()
        if re.search(r"\b(hi|hello|hey|नमस्ते|नमस्कार)\b", t):
            return "greeting"
        if any(k in t for k in ["help", "madad", "सहायता"]):
            return "help"
        if any(k in t for k in ["price", "kitna", "rate", "charges", "कितना"]):
            return "pricing"
        if any(k in t for k in ["cancel", "रद्द"]):
            return "cancel_booking"
        if any(k in t for k in ["reschedule", "time change", "समय बदल"]):
            return "reschedule_booking"
        if any(k in t for k in ["status", "kya hua", "कब आएगा"]):
            return "status_check"
        # service detection
        if self._identify_service(t):
            return "book_service"
        return "other"

    def _identify_service(self, text: str) -> Optional[str]:
        t = (text or "").lower()
        for svc, keys in self.SERVICE_KEYWORDS.items():
            if any(k in t for k in keys):
                return svc
        return None

    async def process(self) -> ChatResponse:
        try:
            intent = self._detect_intent(self.query)
            logger.info(f"Detected intent={intent} for user_id={self.user_id}")

            if intent == "greeting":
                reply = (
                    f"Hi {self.user_name}! I can help you book services (plumber, electrician, cleaner, etc.), "
                    f"check booking status, or cancel/reschedule. What do you need?"
                )
                return ChatResponse(reply=reply, action="greeting")

            if intent == "pricing":
                reply = (
                    "Approximate pricing: plumber/electrician visits start at ₹199. "
                    "Final amount depends on the job. Would you like me to book someone?"
                )
                return ChatResponse(reply=reply, action="pricing")

            if intent == "status_check":
                reply = "Please share your booking ID to check the status (e.g., BK-12345)."
                return ChatResponse(reply=reply, action="status_check")

            if intent == "cancel_booking":
                reply = "Please share your booking ID to cancel the booking."
                return ChatResponse(reply=reply, action="cancel_booking")

            if intent == "reschedule_booking":
                reply = "Please share your booking ID and the new preferred date/time."
                return ChatResponse(reply=reply, action="reschedule_booking")

            if intent == "book_service":
                svc = self._identify_service(self.query) or "general"
                reply = f"Sure. Booking a {svc}. Please share preferred date/time and your flat number."
                return ChatResponse(reply=reply, action="collect_booking_details", data={"service_type": svc})

            # help/other
            reply = (
                "I’m your society assistant. You can say things like: 'Need a plumber today 6 pm', "
                "'Check status BK-12345', or 'Cancel BK-12345'."
            )
            return ChatResponse(reply=reply, action="help")
        except Exception as e:
            logger.exception("Failed to process chat")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process webhook {str(e)}",
            )

    async def chat_base_processor(self) -> ChatResponse:
        # backwards-compatible entrypoint name
        return await self.process()

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