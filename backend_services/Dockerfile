# 1. Base Image
FROM python:3.9-slim

# 2. System Dependencies (Updated to include ffmpeg)
# 'libgl1' is for OpenCV
# 'ffmpeg' is for Audio Conversion (pydub)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 3. Work Directory
WORKDIR /app

# 4. Upgrade PIP
RUN pip install --upgrade pip

# 5. Install CPU-Only PyTorch (Lightweight)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Install TensorFlow (CPU)
RUN pip install --no-cache-dir tensorflow-cpu==2.12.0

# 7. Copy Requirements
COPY requirements.txt .

# 8. Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 9. Copy Application Code
COPY . .

# 10. Start Command
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]