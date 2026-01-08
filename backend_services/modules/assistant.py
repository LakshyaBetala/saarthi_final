# backend_services/modules/assistant.py
import time
from .audio import speak
from .search import google_search_summary
from .vision import detect_objects_and_direction
from .emotion import analyze_emotion
from .utils import get_camera_url, listen_command
# DELETED: import pywhatkit (Docker cannot open browsers)

def continuous_assistant():
    camera_url = get_camera_url()
    
    # Note: In Docker, listen_command() might fail if it tries to use the server's microphone.
    # ideally, audio should be sent from the frontend.
    try:
        command = listen_command()
    except Exception as e:
        print(f"Mic Error: {e}")
        return {"message": "Microphone unavailable on server."}

    # ✅ Skip empty or failed recognition
    if not command or command.strip() == "":
        return {"message": "No command detected. Waiting..."}

    # ✅ Trigger assistant if name is called
    if any(name in command.lower() for name in ["bharat", "bharath", "barat", "bha"]):
        for name in ["bharat", "bharath", "barat", "bha"]:
            command = command.lower().replace(name, "")
        command = command.strip()

        # 🎯 OBJECT + EMOTION
        if "object" in command or "detect" in command or "ahead" in command:
            result = detect_objects_and_direction(camera_url)

            object_labels = [obj["name"] for obj in result["objects"]]
            if object_labels:
                speak("Objects ahead are " + ", ".join(object_labels))
                time.sleep(4)

            speak(result["direction"])
            time.sleep(2)

            return {
                "action": "Object detection",
                "objects": object_labels,
                "direction": result["direction"]
            }

        # 🔍 SEARCH
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching for {query}")
            return google_search_summary(query)

        # ▶️ PLAY YOUTUBE (Fixed for Docker)
        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            
            # Docker cannot open a browser. We return the INTENT to the frontend.
            # The Frontend (React) will handle opening the link.
            return {
                "action": "YouTube", 
                "query": song,
                "url": f"https://www.youtube.com/results?search_query={song}"
            }

        # 🛑 STOP
        elif "stop" in command or "exit" in command:
            speak("Goodbye!")
            return {"message": "Assistant stopped."}

        # ❓ UNKNOWN
        else:
            speak("Command unclear. Please try again.")
            return {"message": "Unrecognized command."}

    # ❌ Not addressed to assistant
    return {"message": "No assistant trigger word detected."}

# backend_services/modules/assistant.py
import time
from .audio import speak
from .search import google_search_summary
from .vision import detect_objects_and_direction
from .emotion import analyze_emotion
from .utils import get_camera_url, listen_command
# DELETED: import pywhatkit (Docker cannot open browsers)

def continuous_assistant():
    camera_url = get_camera_url()
    
    # Note: In Docker, listen_command() might fail if it tries to use the server's microphone.
    # ideally, audio should be sent from the frontend.
    try:
        command = listen_command()
    except Exception as e:
        print(f"Mic Error: {e}")
        return {"message": "Microphone unavailable on server."}

    # ✅ Skip empty or failed recognition
    if not command or command.strip() == "":
        return {"message": "No command detected. Waiting..."}

    # ✅ Trigger assistant if name is called
    if any(name in command.lower() for name in ["bharat", "bharath", "barat", "bha"]):
        for name in ["bharat", "bharath", "barat", "bha"]:
            command = command.lower().replace(name, "")
        command = command.strip()

        # 🎯 OBJECT + EMOTION
        if "object" in command or "detect" in command or "ahead" in command:
            result = detect_objects_and_direction(camera_url)

            object_labels = [obj["name"] for obj in result["objects"]]
            if object_labels:
                speak("Objects ahead are " + ", ".join(object_labels))
                time.sleep(4)

            speak(result["direction"])
            time.sleep(2)

            return {
                "action": "Object detection",
                "objects": object_labels,
                "direction": result["direction"]
            }

        # 🔍 SEARCH
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching for {query}")
            return google_search_summary(query)

        # ▶️ PLAY YOUTUBE (Fixed for Docker)
        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            
            # Docker cannot open a browser. We return the INTENT to the frontend.
            # The Frontend (React) will handle opening the link.
            return {
                "action": "YouTube", 
                "query": song,
                "url": f"https://www.youtube.com/results?search_query={song}"
            }

        # 🛑 STOP
        elif "stop" in command or "exit" in command:
            speak("Goodbye!")
            return {"message": "Assistant stopped."}

        # ❓ UNKNOWN
        else:
            speak("Command unclear. Please try again.")
            return {"message": "Unrecognized command."}

    # ❌ Not addressed to assistant
    return {"message": "No assistant trigger word detected."}