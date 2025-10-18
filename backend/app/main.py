import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agents.gateway_agent import GatewayAgent


# Load configuration values from environment variables
APP_NAME = os.getenv("APP_NAME")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")
origins = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]

logging.info(f"Allowed CORS origins: {origins}") 

# Store message as part of data validation and serialization
class ChatRequest(BaseModel):
    message: str

# Create FastAPI app
app = FastAPI(title=APP_NAME)

# Enable CORS so frontend (different origin) can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME}

# Chat API: forwards user message to DukeGPT model
@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Chat using LLM proxy. Uses the Responses API.
    """
    gateway_agent = GatewayAgent()
    content = request.message
    decision = gateway_agent.get_agent(content)

    if decision["type"] == "ERROR":
        reply = f"Error: {content}"
    else:
        agent = decision["agent"]
        reply = agent.handle_request(decision["answer"], content)
    # Ensure string return
    if isinstance(reply, dict):
        # LangChain returns {'text': "..."} sometimes
        reply = reply.get("text") or str(reply)

    return {"reply": str(reply)}
