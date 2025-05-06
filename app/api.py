import asyncio
import json
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

async def process_prompt(prompt: str, max_tokens: int) -> AsyncGenerator[str, None]:
    """Process the prompt and generate streaming response"""
    # Simulate processing the prompt and generating tokens
    for i in range(max_tokens):
        # In a real application, this would be your actual LLM processing
        token = f"token_{i}"
        data = {
            "id": i,
            "event": "token",
            "data": token,
            "prompt": prompt
        }
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.1)  # Simulate processing time

@app.post("/process")
async def process_endpoint(request: PromptRequest):
    """Endpoint to process prompts and stream results"""
    return StreamingResponse(
        process_prompt(request.prompt, request.max_tokens),
        media_type="text/event-stream"
    )

@app.get("/stream")
async def stream_endpoint():
    """SSE streaming endpoint"""
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

async def event_generator() -> AsyncGenerator[str, None]:
    """Async generator for SSE events"""
    for i in range(10):  # Example: generate 10 events
        # Construct SSE format data
        data = {
            "id": i,
            "event": "message",
            "data": f"This is message {i+1}"
        }
        # Format output according to SSE specification
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)  # Send one message per second

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to SSE API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
