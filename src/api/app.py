from fastapi import FastAPI
from pydantic import BaseModel
from src.llm.prompt_handler import get_greeting_response, generate_test

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

class CodeRequest(BaseModel):
    language: str
    method_code: str

@app.post("/chat/")
def chat(request: ChatRequest):
    response = get_greeting_response(request.prompt)
    return {"response": response}

@app.post("/generate-test/")
async def generate_test_api(request: CodeRequest):
    return generate_test(request.language, request.method_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)