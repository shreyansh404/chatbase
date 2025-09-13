#Third party imports
from fastapi import FastAPI, HTTPException, status

#Local imports
from chatbase.models.chat_base_model import GLPIWebhookPayload
from chatbase.service.chat_builder_processor import ChatBaseProcessor

app = FastAPI()

@app.post("/")
async def webhook_processor(payload_dict: dict):
    try:
        payload = GLPIWebhookPayload(**payload_dict)
        processor = ChatBaseProcessor(payload)
        result = await processor.process()
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to process webhook {str(e)}")