import re

SERVICE_MAP = {
    "plumber": ["plumber", "plumbing", "प्लम्बर", "nal", "leak", "टap", "गीजर"],
    "electrician": ["electric", "इलेक्ट्रीशियन", "fan", "light", "switch", "wiring"],
    "carpenter": ["carpenter", "कारपेंटर", "wood", "door", "hinge", "shelf"],
    "cleaner": ["clean", "क्लीन", "सफाई", "safaai", "deep clean"],
    "pest_control": ["pest", "cockroach", "termite", "bed bug", "कीड़े", "मक्खी"],
    "guard": ["guard", "security", "सिक्योरिटी"]
}

def fast_path_intent(text: str) -> Optional[IntentResult]:
    t = text.lower()
    # Greetings / help
    if re.search(r"\b(hi|hello|hey|नमस्ते|नमस्कार)\b", t):
        return IntentResult(intent="greeting")
    if "help" in t or "madad" in t or "सहायता" in t:
        return IntentResult(intent="help")
    if "price" in t or "kitna" in t or "rate" in t or "charges" in t or "कितना" in t:
        return IntentResult(intent="pricing")
    if "cancel" in t or "रद्द" in t:
        return IntentResult(intent="cancel_booking")
    if "reschedule" in t or "time change" in t or "समय बदल" in t:
        return IntentResult(intent="reschedule_booking")
    if "status" in t or "kya hua" in t or "कब आएगा" in t:
        return IntentResult(intent="status_check")

    # Book service easy detection
    for svc, keys in SERVICE_MAP.items():
        if any(k in t for k in keys):
            return IntentResult(intent="book_service", booking=BookingSlots(service_type=svc))  # fill more via LLM later

    return None