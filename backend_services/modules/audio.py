# backend_services/modules/audio.py
from gtts import gTTS
import os
import uuid

# DELETED: from playsound import playsound (Docker cannot play sound)

def speak(text, save_audio=True):
    """
    Convert text to speech and return the file path.
    In Docker/Server mode, we ALWAYS save the file and send it to the frontend.
    """
    audio_path = f"audio_{uuid.uuid4()}.mp3"
    
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"❌ Audio Generation Error: {e}")
        return None