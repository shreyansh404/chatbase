import uvicorn

if __name__ == "__main__":
    uvicorn.run("webhook_processor:app", host="0.0.0.0", port=8946, reload=True)