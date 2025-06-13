from gtts import gTTS
import tempfile

def text_to_speech(text: str) -> str:
    tts = gTTS(text)
    file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(file_path)
    return file_path
