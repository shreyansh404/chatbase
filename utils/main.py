import uvicorn

if __name__ == "__main__":
    uvicorn.run("chat_base_webhook:app", host="0.0.0.0", port=8946)