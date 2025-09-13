from typing import List, Optional
import re

SERVICE_MAP = {
    "plumber": ["plumber", "plumbing", "प्लम्बर", "nal", "leak", "टap", "गीजर", "tap", "leak", "water", "water problem"],
    "electrician": ["electric", "इलेक्ट्रीशियन", "fan", "light", "switch", "wiring", "electrician", "power"],
    "carpenter": ["carpenter", "कारपेंटर", "wood", "door", "hinge", "shelf"],
    "cleaner": ["clean", "क्लीन", "सफाई", "safaai", "deep clean", "cleaning", "cleaner"],
    "pest_control": ["pest", "cockroach", "termite", "bed bug", "कीड़े", "मक्खी"],
    "guard": ["guard", "security", "सिक्योरिटी"],
    "greeting": ['hi', 'hello', 'hey', 'good morning', 'namaste', 'namaskar', "नमस्कार",'नमस्ते'],
    "check_statis": ['status', 'check', 'progress', 'update'],
}

def detect_intent(user_query: str) -> Optional[List[str]]:
    """Return list of matching intents/services from user_query."""
    q = user_query.lower()
    matches = []

    for service, keywords in SERVICE_MAP.items():
        for kw in keywords:
            if kw.lower() in q:
                matches.append(service)
                break

    return matches or ["general"]