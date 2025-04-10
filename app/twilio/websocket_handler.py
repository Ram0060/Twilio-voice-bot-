from fastapi import WebSocket
from app.conversation.session import ConversationSession
from app.utils.gcs_utils import upload_conversation_to_gcs
from app.config import GCS_BUCKET_NAME
from app.utils.audio_utils import transcribe_audio_chunk
from app.llm.openai_llm import get_llm_response
from app.tts.tts_service import generate_tts_audio
import httpx
import base64
import asyncio
import time

async def handle_twilio_websocket(websocket: WebSocket):
    await websocket.accept()
    print("🔌 WebSocket connection established")

    session = ConversationSession()
    audio_data = bytearray()  # Collect full audio here

    async def process_audio_data():
        nonlocal audio_data
        try:
            if audio_data:
                transcript = transcribe_audio_chunk(bytes(audio_data))
                print(f"🗣️ User said: {transcript}")
                session.add_user_input(transcript)

                reply, updated_history = get_llm_response(transcript, session.chat_history)
                session.chat_history = updated_history
                print(f"🤖 Assistant replied: {reply}")
                session.add_assistant_reply(reply)

                filename = generate_tts_audio(reply)
                session.add_audio_response(filename)
                print(f"🔊 TTS generated and stored as: {filename}")

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://localhost:8000/twilio/play_next",
                        data={"filename": filename}
                    )
                    if response.status_code == 200:
                        print(f"📞 Triggered Twilio playback for {filename}")
                    else:
                        print(f"⚠️ Playback trigger failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error during processing: {e}")

    try:
        while True:
            message = await websocket.receive_json()

            if message.get("event") == "media":
                payload_b64 = message["media"]["payload"]
                chunk = base64.b64decode(payload_b64)
                audio_data.extend(chunk)  # Collect all audio data into audio_data
                print(f"🎧 Received audio chunk ({len(chunk)} bytes)")

            elif message.get("event") == "stop":
                print("🛑 Received stop event from Twilio")
                # Process the full audio once stop event is received
                await process_audio_data()
                audio_data.clear()  # Clear buffer after processing

    except Exception as e:
        print(f"❌ WebSocket error: {e}")

    finally:
        upload_conversation_to_gcs(session, bucket_name=GCS_BUCKET_NAME)
        try:
            if not websocket.client_state.name == "DISCONNECTED":
                await websocket.close()
        except Exception as close_err:
            print(f"⚠️ WebSocket already closed or error closing: {close_err}")
        print("🛑 WebSocket closed and session uploaded")
