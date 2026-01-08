# backend_services/modules/utils.py
import cv2  # <--- Added this (Crucial for Vision)
import speech_recognition as sr
from pydub import AudioSegment
import os

# Default to 0 (Webcam)
camera_url = 0

def get_camera_url():
    return camera_url

def set_camera_url(url):
    global camera_url
    # If the URL is a number (like "0"), convert it to an integer
    try:
        camera_url = int(url)
    except ValueError:
        camera_url = url

# ✅ THE MISSING FUNCTION
def capture_frame(url):
    try:
        cap = cv2.VideoCapture(url)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        return None
    except Exception as e:
        print(f"Camera Error: {e}")
        return None

def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    
    # Convert 'webm' or 'mp3' to 'wav' for SpeechRecognition
    try:
        # We need to ensure ffmpeg is installed in Docker for this line to work
        if not file_path.endswith(".wav"):
            audio = AudioSegment.from_file(file_path)
            file_path = "converted_temp.wav"
            audio.export(file_path, format="wav")
            is_converted = True
        else:
            is_converted = False

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
        if is_converted:
            os.remove(file_path) # Cleanup
            
        return text
    except Exception as e:
        print(f"❌ Transcription Error: {e}")
        return ""

def listen_command():
    return ""