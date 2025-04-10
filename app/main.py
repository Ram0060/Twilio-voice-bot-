from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, JSONResponse
from app.twilio.websocket_handler import handle_twilio_websocket
from app.twilio.webhook import generate_twiml_stream, generate_twiml_play
import os

public_base_url = os.getenv("PUBLIC_BASE_URL")
app = FastAPI()

# CORS for dev/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Change in production
    allow_credentials=True,                 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Voice AI Agent is running locally 🎙️"}

@app.websocket("/twilio/stream")
async def websocket_endpoint(websocket: WebSocket):
    await handle_twilio_websocket(websocket)

@app.get("/twilio/audio/{filename}")
async def serve_audio(filename: str):
    file_path = os.path.join("tts_audio", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return JSONResponse(content={"error": "File not found"}, status_code=404)

@app.post("/twilio/response")
async def twilio_start_stream(request: Request):
    # ✅ Log when Twilio redirects to this endpoint
    print("📥 Twilio redirected back to /twilio/response")

    # ✅ Always use fixed public ngrok domain
    stream_url = "wss://21b3-2601-47-4600-18c0-bc6e-1ef1-fe10-941.ngrok-free.app/twilio/stream"

    print(f"📡 Twilio will stream audio to: {stream_url}")
    twiml = generate_twiml_stream(stream_url)
    return Response(content=twiml, media_type="application/xml")

@app.post("/twilio/play_next")
async def play_next_audio(request: Request):
    form = await request.form()
    filename = form.get("filename")

    if not filename:
        return JSONResponse(content={"error": "Filename not provided"}, status_code=400)

    public_base_url = "https://0c02-2601-47-4600-18c0-bc6e-1ef1-fe10-941.ngrok-free.app"

    audio_url = f"{public_base_url}/twilio/audio/{filename}"
    redirect_url = f"{public_base_url}/twilio/response"

    print(f"🔁 Playing: {audio_url} → then redirecting to {redirect_url}")
    twiml = generate_twiml_play(audio_url, redirect_url=redirect_url)
    return Response(content=twiml, media_type="application/xml")
