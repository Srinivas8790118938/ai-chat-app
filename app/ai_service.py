from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(user_message: str, chat_history: list = None):

    try:
        # If no history passed, create fresh one
        if chat_history is None:
            chat_history = [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ]

        # Add user message
        chat_history.append({"role": "user", "content": user_message})

        # Call Groq
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="llama-3.1-8b-instant"
        )

        reply = chat_completion.choices[0].message.content

        # Add assistant reply to history
        chat_history.append({"role": "assistant", "content": reply})

        return reply, chat_history

    except Exception as e:
        return f"Error: {str(e)}", chat_history
