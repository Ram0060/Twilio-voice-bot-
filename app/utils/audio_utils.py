import whisper
import tempfile
import subprocess
from pathlib import Path
import os

model = whisper.load_model("base")

def transcribe_audio_chunk(audio_bytes: bytes) -> str:
    try:
        print("📥 Received audio chunk for transcription")

        # Write raw audio bytes to temp input
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ulaw") as ulaw_file:
            ulaw_file.write(audio_bytes)
            ulaw_path = ulaw_file.name
        print(f"💾 Saved raw ULaw audio: {ulaw_path} ({len(audio_bytes)} bytes)")

        # Convert ULaw to WAV using ffmpeg
        wav_path = ulaw_path.replace(".ulaw", ".wav")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "mulaw", "-ar", "8000", "-ac", "1", "-i", ulaw_path,
            "-ar", "16000", wav_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if not os.path.exists(wav_path):
            raise RuntimeError("ffmpeg failed to produce WAV output")

        print(f"🎧 Converted to WAV: {wav_path} ({os.path.getsize(wav_path)} bytes)")

        # Transcribe with Whisper
        result = model.transcribe(wav_path)
        transcript = result.get("text", "").strip()
        print(f"📝 Whisper transcript: {transcript}")

        return transcript

    except Exception as e:
        print(f"❌ Whisper transcription error: {e}")
        return ""

    finally:
        # Clean up temp files
        try:
            Path(ulaw_path).unlink(missing_ok=True)
            Path(wav_path).unlink(missing_ok=True)
            print("🧹 Cleaned up temporary audio files")
        except Exception as cleanup_err:
            print(f"⚠️ Cleanup failed: {cleanup_err}")
