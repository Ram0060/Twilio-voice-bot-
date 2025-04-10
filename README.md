# Twilio-voice-bot

🗣️ OpenAI Voice Agent (Cloud-Native)
A fully cloud-native, real-time voice AI agent that handles phone calls using Twilio, processes spoken input with OpenAI GPT, and replies with natural-sounding audio. The conversation (transcript + audio) is saved to Google Cloud Storage for recordkeeping or analysis.

🚀 Features
📞 Twilio integration for receiving voice calls

🎙️ Real-time audio transcription using Whisper

🧠 Conversational intelligence via OpenAI GPT

🔊 Text-to-speech response with audio playback

☁️ Upload transcripts and audio to Google Cloud Storage

♻️ Supports multi-turn conversations with silence detection

🐳 Dockerized for easy deployment


Tech Stack
FastAPI — Web server for Twilio webhooks and WebSocket

Twilio — Voice call handling and <Stream> support

OpenAI GPT — Language model for generating responses

TTS — Converts GPT responses to speech (OpenAI Voice or gTTS)

Whisper — Speech-to-text for caller input

Google Cloud Storage (GCS) — Uploads transcriptions and audio logs

Docker — Containerized deployment


⚙️ Configure Environment Variables

OPENAI_API_KEY=your_openai_key
GCS_BUCKET_NAME=your_bucket
TWILIO_AUTH_TOKEN=your_token
TWILIO_ACCOUNT_SID=your_sid

🐳 Docker Deployment
1. Build the Docker image

docker build -t voice-ai-agent .

2. Run the container
docker run -p 8000:8000 --env-file .env voice-ai-agent

☁️ Cloud Run 
Go to Twilio Console

Create a new phone number

Set the Voice webhook 

Ensure Twilio Streaming is enabled for real-time conversation



🧪 Test It Out (Multi-Turn Voice Conversation)
""" 
Call your Twilio number
Your call will be routed to the AI agent hosted on Google Cloud Run.

Speak naturally — ask a question or give a prompt
Example:

"Hey, can you help me schedule a meeting for tomorrow?"

The agent will respond using natural TTS audio
Example:

"Sure! What time would you like the meeting to be?"

Continue the conversation in real-time
You can keep talking — the agent detects silences and replies accordingly.
Example:

"Let's do 3 p.m. with John from marketing."
"Got it! I'll set a reminder for tomorrow at 3 p.m. with John."

Finish the call when you're done
Hang up at any time. The session will end and finalize storage.

Review the conversation in your GCS bucket

📜 Full transcription saved as .txt or .json

🔊 Audio responses and user input saved as .mp3 or .wav
"""




