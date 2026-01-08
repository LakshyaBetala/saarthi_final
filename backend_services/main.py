# backend_services/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from modules.assistant import continuous_assistant, process_audio_command
from modules.utils import set_camera_url
import os
import shutil

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve generated audio files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"status": "Saarthi AI Backend Running 🚀"}

@app.post("/set_camera_url")
def update_camera(url: str):
    set_camera_url(url)
    return {"message": "Camera URL updated"}

# ✅ THE NEW ENDPOINT: Accepts audio file from Frontend
@app.post("/assistant/audio")
async def audio_command(file: UploadFile = File(...)):
    # 1. Save the incoming audio file temporarily
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Process the audio file (Speech -> Text -> AI Action)
    response = process_audio_command(temp_filename)
    
    # 3. Clean up
    os.remove(temp_filename)
    
    return response

# Keep this for testing, but the /assistant/audio is the main one now
@app.get("/assistant/listen")
def listen():
    return continuous_assistant()