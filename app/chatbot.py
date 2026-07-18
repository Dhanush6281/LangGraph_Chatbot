import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_response(messages):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=messages
    )
    return response.text


def build_messages(chat_history):
    contents = []

    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"

        contents.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            }
        )

    return contents