# Third Party
from google.adk.agents import Agent

#Local imports
from chatbase.log import get_logger
from chatbase.service.chat_builder_processor import ChatBaseProcessor

logger = get_logger()

class ChatBaseAgent(Agent):
    def __init__(self, user_id, session_id="default_session", language="en", model="Gemini 2.5flash", app_name= None):
        self.model = model
        self.user_id = user_id
        self.language = language
        self.session_id = session_id
        self.app_name = app_name

    def _create_agent(self, system_prompt):

        agent = Agent(
            app_name=self.app_name,
            init_session=system_prompt,
            model=self.model,
            instruction="You are a society assistant on WhatsApp. Help users book plumber/electrician/etc., check status, or cancel.",
            tools=[ChatBaseProcessor.book_service, ChatBaseProcessor.check_status]
        )
        return agent

    async def _ensure_session_exists(self):
        """Ensure the ADK session exists, create if needed."""
        # Use a flag to ensure the session is created only once per instance.
        if self._session_initialized:
            return

        try:
            await self.session_service.create_session(
                app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
            )
            logger.info("ADK session created successfully.")
            self._session_initialized = True
        except Exception as e:
            # The SessionAlreadyExistsError is expected in certain scenarios.
            # We can safely ignore it and proceed.
            logger.error(f"Error creating session: {e}")
            self._session_initialized = True
            pass

    async def llm_response(self, query):
        try:
            pass
        except Exception as e:
            ra