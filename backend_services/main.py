from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from modules.assistant import continuous_assistant, process_audio_command
from modules.utils import set_camera_url, get_camera_url
import os
import shutil
import uvicorn

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for audio files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"status": "Saarthi AI Backend Running 🚀"}

@app.post("/set_camera_url")
def update_camera(url: str = Form(...)):
    # Handle if user sends just IP or full URL
    if not url.startswith("http"):
         url = f"http://{url}:8080/video"
    set_camera_url(url)
    return {"message": "Camera URL updated", "url": url}

# ✅ THE MISSING ENDPOINT: Accepts audio file from Frontend
@app.post("/assistant/audio")
async def audio_command(file: UploadFile = File(...)):
    # 1. Save the incoming audio file temporarily
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Process the audio file (Speech -> Text -> AI Action)
    try:
        response = process_audio_command(temp_filename)
    except Exception as e:
        print(f"Error processing audio: {e}")
        response = {"message": "Error processing audio"}
    finally:
        # 3. Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
    return response

# Legacy endpoint (kept for safety)
@app.get("/assistant/listen")
def listen_for_command():
    return continuous_assistant()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)