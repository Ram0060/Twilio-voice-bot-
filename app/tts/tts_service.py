import os
import shutil

AUDIO_OUTPUT_DIR = "tts_audio"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def generate_tts_audio(src_path: str, prefix: str = "") -> str:
    """
    Optionally renames audio received from LLM (already Twilio-safe).

    Args:
        src_path (str): Path to the file saved from LLM (e.g. /tmp/audio.mp3).
        prefix (str): Optional filename prefix.

    Returns:
        str: New filename after renaming/moving.
    """
    filename = f"{prefix}{os.path.basename(src_path)}"
    final_path = os.path.join(AUDIO_OUTPUT_DIR, filename)

    shutil.move(src_path, final_path)
    return filename
