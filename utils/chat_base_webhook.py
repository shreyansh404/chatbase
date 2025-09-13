#Third party imports
from fastapi import FastAPI, HTTPException, status

#Local imports
from chatbase.models.chat_base_model import GLPIWebhookPayload
from chatbase.service.chat_builder import chat_base_processor

app = FastAPI()


@app.post("/", description="Chatbase Webhook")
async def chatbase_webhook(webhook_payload: GLPIWebhookPayload):
    """

    :param webhook:
    :return:
    """
    try:
        chat_base_response = await chat_base_processor(webhook_payload)
        return chat_base_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to process webhook {str(e)}")