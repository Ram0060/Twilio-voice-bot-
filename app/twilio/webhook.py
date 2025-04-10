from fastapi import Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse

def generate_twiml_stream(stream_url: str) -> str:
    """
    TwiML to greet and start Twilio audio stream, then pause to keep call alive.
    """
    response = VoiceResponse()
    response.say("Hi! I'm your AI assistant. Let's chat.")
    response.start().stream(url=stream_url)

    # ⏸️ Keep the call open while the stream is active
    response.pause(length=60)  # long enough to listen
    return str(response)

def generate_twiml_play(audio_url: str, redirect_url: str = None) -> str:
    """
    TwiML that plays TTS audio and redirects to restart streaming.
    """
    response = VoiceResponse()
    response.play(audio_url)

    # ⏳ Small pause before redirecting back to streaming
    response.pause(length=3)

    # 🔁 Return to the stream after playback
    if redirect_url:
        response.redirect(redirect_url)

    return str(response)
