from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import random
import uvicorn

app = FastAPI()

# Request model
class LLMRequest(BaseModel):
    request_id: str
    email_content: str

# Response model
class LLMResponse(BaseModel):
    llm_response: Optional[dict] = Field(default=None, title="LLM Response")

@app.post("/process-llm", response_model=LLMResponse)
async def process_llm(request: LLMRequest):
    """
    Dummy LLM service that returns a random classification.
    """
    categories = ["spam", "ham", "promotion", "important"]
    llm_output = {
        "category": random.choice(categories),
        "confidence": round(random.uniform(0.7, 0.99), 2),
    }

    return LLMResponse(llm_response=llm_output)

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
