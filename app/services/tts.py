from __future__ import annotations

import io
from gtts import gTTS


class TTSService:
    def synthesize(self, text: str, lang: str = "en") -> bytes:
        tts = gTTS(text=text, lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()


