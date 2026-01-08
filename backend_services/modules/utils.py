import cv2
import speech_recognition as sr
from pydub import AudioSegment
import os
import requests
import re

camera_url = 0

def get_camera_url():
    return camera_url

def set_camera_url(url):
    global camera_url
    try:
        camera_url = int(url)
    except ValueError:
        camera_url = url

def capture_frame(url):
    try:
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        return None
    except Exception:
        return None

def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    converted_path = "converted_temp.wav"
    is_converted = False
    
    try:
        if not file_path.endswith(".wav"):
            audio = AudioSegment.from_file(file_path)
            audio.export(converted_path, format="wav")
            file_path = converted_path
            is_converted = True

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
        return text
    except Exception as e:
        print(f"❌ Transcription Error: {e}")
        return ""
    finally:
        if is_converted and os.path.exists(converted_path):
            os.remove(converted_path)

# ✅ NEW: Find the first video URL so we can AUTO-PLAY it
def get_first_youtube_video(query):
    try:
        # Search YouTube (HTML)
        search_url = f"https://www.youtube.com/results?search_query={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        
        # Regex to find the first video ID
        # Look for "videoId":"(11 chars)"
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
        
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
        
        # Fallback to search page if scraping fails
        return search_url
    except Exception:
        return f"https://www.youtube.com/results?search_query={query}"