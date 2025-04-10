import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Tuple
import uuid

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")  # Make sure this is set

AUDIO_OUTPUT_DIR = "tts_audio"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def get_llm_response(
    user_message: str,
    history: List[Dict[str, str]] = None
) -> Tuple[str, str]:
    """
    Uses OpenAI Assistants API with voice=True to get text + audio response.
    
    Returns:
        Tuple[str, str]: Text reply and saved filename of MP3 audio.
    """
    if not ASSISTANT_ID:
        raise ValueError("Missing OPENAI_ASSISTANT_ID in environment.")

    # Create a thread and add the user message
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Run the assistant with voice support
    run = openai.beta.threads.runs.create_and_poll(
        assistant_id=ASSISTANT_ID,
        thread_id=thread.id,
        tools=[],
        voice=True  # 🔥 This makes it return MP3 audio
    )

    # Extract the assistant reply message
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    assistant_message = next(
        (m for m in messages.data if m.role == "assistant"), None
    )

    if not assistant_message:
        raise RuntimeError("No assistant reply found.")

    text_reply = assistant_message.content[0].text.value
    audio_file = assistant_message.content[1].audio.file  # This is a `file` object

    # Download the audio bytes
    audio_data = openai.files.retrieve_content(audio_file.id)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(audio_data)

    print(f"✅ LLM returned audio + text: {filename}")
    return text_reply, filename
