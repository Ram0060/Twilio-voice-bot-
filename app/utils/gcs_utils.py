import json
from google.cloud import storage
import os

def upload_conversation_to_gcs(session, bucket_name: str):
    # Init GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    folder_prefix = f"conversations/{session.session_id}/"

    # Upload transcript JSON
    transcript_blob = bucket.blob(f"{folder_prefix}transcript.json")
    transcript_blob.upload_from_string(
        json.dumps(session.user_transcripts, indent=2),
        content_type="application/json"
    )

    # Upload assistant replies
    reply_blob = bucket.blob(f"{folder_prefix}assistant_replies.json")
    reply_blob.upload_from_string(
        json.dumps(session.assistant_replies, indent=2),
        content_type="application/json"
    )

    # Upload audio files from tts_audio folder
    for idx, filename in enumerate(session.audio_responses):
        audio_path = os.path.join("tts_audio", filename)
        if os.path.exists(audio_path):
            audio_blob = bucket.blob(f"{folder_prefix}audio_{idx}.mp3")
            audio_blob.upload_from_filename(audio_path, content_type="audio/mpeg")
            print(f"✅ Uploaded: {filename} to GCS")
        else:
            print(f"⚠️ File not found: {audio_path}")

    print(f"✅ Uploaded session {session.session_id} to GCS bucket: {bucket_name}")
