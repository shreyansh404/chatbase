# Third Party
from google.adk.agents import Agent
from google.adk.runners import Runner
from pprint import pformat
from google.adk.sessions import InMemorySessionService
from google.genai import types

#Local imports
from chatbase.log import get_logger
from chatbase.service.chat_builder_processor import ChatBaseProcessor
from chatbase.models.llm_response import ChatResponse

logger = get_logger()

class ChatBaseAgent(Agent):
    def __init__(self, user_id, session_id="default_session", language="en", model="gemini-2.5-flash", app_name= "society-assistant"):
        self.model = model
        self.user_id = user_id
        self.language = language
        self.session_id = session_id
        self.app_name = app_name

    def _create_agent(self):

        agent = Agent(
            app_name=self.app_name,
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

    async def send_to_llm(self, instruction: str):
        """
        Send rendered prompts to the LLM using Agent, and yield the response.
        """
        await self._ensure_session_exists()

        # Create the Agent and Runner within the same async context
        agent = self._create_agent()
        runner_agent = Runner(
            agent=agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )


        async for event in runner_agent.run_async(
            user_id=self.user_id,
            session_id=self.session_id,
            new_message=types.Content(
                role="user", parts=[types.Part(text=instruction)]
            ),
        ):
            # Handle events...
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call:
                        formatted_call = f"```python\n{pformat(part.function_call.model_dump(exclude_none=True), indent=2, width=80)}\n```"
                        response = ChatResponse(
                            role="assistant",
                            content=f"🛠️ **Tool Call: {part.function_call.name}**\n{formatted_call}",
                        )
                        yield response.json()

                    elif part.function_response:
                        response_content = part.function_response.response
                        if (
                            isinstance(response_content, dict)
                            and "response" in response_content
                        ):
                            formatted_response_data = response_content["response"]
                        else:
                            formatted_response_data = response_content
                        formatted_response = f"```json\n{pformat(formatted_response_data, indent=2, width=80)}\n```"
                        response = ChatResponse(
                            role="assistant",
                            content=f"⚡ **Tool Response from {part.function_response.name}**\n{formatted_response}",
                        )
                        yield response.json()

            if event.is_final_response():
                final_response_text = ""
                if event.content and event.content.parts:
                    final_response_text = "".join(
                        [p.text for p in event.content.parts if p.text]
                    )
                elif event.actions and event.actions.escalate:
                    final_response_text = f'Agent escalated: {event.error_message or "No specific message."}'

                if final_response_text:
                    response = ChatResponse(
                        role="assistant", content=final_response_text
                    )
                    yield response.json()
                break