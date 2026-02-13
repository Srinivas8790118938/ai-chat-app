from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_service import get_ai_response

app = FastAPI()

# Store chat history in memory (temporary)
chat_sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    # Get existing session history
    history = chat_sessions.get(request.session_id)

    # Get AI response
    reply, updated_history = get_ai_response(request.message, history)

    # Save updated history
    chat_sessions[request.session_id] = updated_history

    return {"response": reply}
