import time
from .audio import speak
from .search import google_search_summary
from .vision import detect_objects_and_direction
from .emotion import analyze_emotion
from .utils import get_camera_url, transcribe_audio_file, get_first_youtube_video
import wikipedia

def process_audio_command(audio_file_path):
    camera_url = get_camera_url()
    
    # 1. Transcribe
    full_command = transcribe_audio_file(audio_file_path)
    print(f"🎤 Original: {full_command}")

    if not full_command:
        return {"voice_response": "I didn't hear anything."}

    # 2. Cleanup: Remove "Bharat" from the start to get the raw intent
    # Example: "Bharat play believer" -> "play believer"
    cleaned_command = full_command.lower()
    for name in ["bharat", "bharath", "barat"]:
        cleaned_command = cleaned_command.replace(name, "")
    
    cleaned_command = cleaned_command.strip()
    print(f"🧠 Processed: {cleaned_command}")

    # 3. Logic Routing

    # 🎯 OBJECT + EMOTION
    if any(w in cleaned_command for w in ["detect", "object", "look", "see"]):
        vision_result = detect_objects_and_direction(camera_url)
        emotion_result = analyze_emotion(camera_url)
        
        objects = [obj["name"] for obj in vision_result.get("objects", [])]
        emotion = emotion_result.get("emotion", "neutral")
        
        response_text = ""
        if objects:
            response_text += f"I see {', '.join(objects)}. "
        else:
            response_text += "I don't see clear objects. "
            
        response_text += vision_result.get("direction", "") + ". "
        
        if emotion != "neutral":
            response_text += f"You look {emotion}."

        return {
            "action": "Vision",
            "voice_response": response_text,
            "data": {"objects": objects, "emotion": emotion}
        }

    # ▶️ YOUTUBE (Auto-Play First Video)
    elif "play" in cleaned_command:
        # "play believer" -> "believer"
        song = cleaned_command.replace("play", "").strip()
        
        # Scrape the FIRST video URL
        video_url = get_first_youtube_video(song)
        
        return {
            "action": "YouTube",
            "voice_response": f"Playing {song} on YouTube.",
            "url": video_url
        }

    # 🔍 SEARCH (Wikipedia First -> Google Fallback)
    elif "search" in cleaned_command or "who is" in cleaned_command or "what is" in cleaned_command:
        query = cleaned_command.replace("search", "").strip()
        
        try:
            # Try Wikipedia (2 sentences)
            summary = wikipedia.summary(query, sentences=2)
            # Ensure comma separation if needed (though wiki usually has grammar)
            voice_text = f"According to Wikipedia, {summary}"
        except:
            # Fallback to Google
            google_res = google_search_summary(query)
            voice_text = google_res.get("summary", "I couldn't find information on that.")

        return {
            "action": "Search",
            "voice_response": voice_text
        }

    # 🛑 STOP
    elif "stop" in cleaned_command or "exit" in cleaned_command:
        return {"action": "Stop", "voice_response": "Goodbye."}

    # ❓ UNKNOWN
    else:
        return {
            "action": "Unknown",
            "voice_response": "I didn't understand. Say 'Bharat play music' or 'Bharat detect'."
        }

def continuous_assistant():
    return {}