
class PromptBuilder:
    async def plumber_service_prompt_builder(self, query: str):
        intent_prompt = f"""
    Analyze this housing society resident query and classify the intent.
    
    Available intents:
    - BOOK_PLUMBER: Request plumber services
    - BOOK_ELECTRICIAN: Request electrician services  
    - BOOK_HOUSEKEEPING: Request cleaning services
    - BOOK_MAINTENANCE: Request maintenance services
    - CHECK_STATUS: Check status of existing requests
    - CHECK_BILLS: Inquire about bills/payments
    - VISITOR_MANAGEMENT: Register/manage visitors
    - SOCIETY_INFO: Ask about society information
    - COMPLAINT: File complaints
    - GREETING: General greetings
    - HELP: Ask for help/menu
    - UNKNOWN: Cannot determine intent
    
    Query: "{query}"
    
    Respond with only the intent name and confidence score (0-1):
    Format: INTENT_NAME|confidence_score
    """
        return intent_prompt
