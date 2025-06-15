from gtts import gTTS
import os
import uuid

def text_to_speech(text: str, lang: str = "en") -> str:
    if not text.strip():
        raise ValueError("Text is empty")

    filename = f"{uuid.uuid4()}.mp3"
    output_dir = "generated_audio"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(path)
    return path
