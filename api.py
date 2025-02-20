from fastapi import FastAPI
from pydantic import BaseModel
from prompt.prompt_handler import get_greeting_response
from search import search_similar_method

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str  

class MethodRequest(BaseModel):
    language: str
    method_code: str  

@app.post("/chat/")
def chat(request: ChatRequest):
    response = get_greeting_response(request.prompt)
    return {"response": response}

@app.post("/generate-test/")
def generate_test(request: MethodRequest):
    """API to generate a unit test for a given method."""
    test_case = search_similar_method(request.method_code)

    if test_case:
        return {"status": "success", "unit_test": test_case}
    else:
        # If no match is found, you can later integrate an LLM-generated test case
        return {"status": "error", "message": "No similar test case found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)