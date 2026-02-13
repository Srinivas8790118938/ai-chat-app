from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ai_service import get_ai_response


app = FastAPI()

# ----- CORS Settings -----
origins = [
    "http://127.0.0.1:5500",  # Frontend if using Live Server
    "http://localhost:5500",  # Also allow localhost
    "http://127.0.0.1:8000",  # Optional: backend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allow all headers
)
# ---------------------------

# Store chat history in memory
chat_sessions = {}

# Pydantic model for request
class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Handle chat request:
    - Maintain per-session history
    - Call AI service
    - Return AI response
    """

    # Get existing history or start fresh
    history = chat_sessions.get(request.session_id)

    # Get AI response
    reply, updated_history = get_ai_response(request.message, history)

    # Save updated history
    chat_sessions[request.session_id] = updated_history

    # Return as JSON
    return {"response": reply}
