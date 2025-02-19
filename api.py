from fastapi import FastAPI
from pydantic import BaseModel
from prompt.prompt_handler import get_greeting_response

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str  # Ensure the input has a "prompt" field

@app.post("/chat/")
def chat(request: ChatRequest):
    response = get_greeting_response(request.prompt)
    return {"response": response}