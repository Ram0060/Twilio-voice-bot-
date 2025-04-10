import uuid
import datetime

class ConversationSession:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.datetime.utcnow().isoformat()
        self.user_transcripts = []
        self.assistant_replies = []
        self.audio_responses = []  # Store filenames now

        # 🔁 Track full conversation context for Chat API
        self.chat_history = [
            {
                "role": "system",
                "content": "You are a helpful voice assistant."
            }
        ]

    def add_user_input(self, text: str):
        timestamped = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "text": text
        }
        self.user_transcripts.append(timestamped)
        self.chat_history.append({"role": "user", "content": text})

    def add_assistant_reply(self, text: str):
        timestamped = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "text": text
        }
        self.assistant_replies.append(timestamped)
        self.chat_history.append({"role": "assistant", "content": text})

    def add_audio_response(self, filename: str):
        self.audio_responses.append(filename)

    def export(self):
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "user_transcripts": self.user_transcripts,
            "assistant_replies": self.assistant_replies,
            "audio_response_count": len(self.audio_responses),
            "chat_history": self.chat_history
        }
