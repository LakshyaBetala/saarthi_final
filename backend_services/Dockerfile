# 1. Base Image: Use Bullseye (Stable Linux for ML)
FROM python:3.9-slim-bullseye

# 2. System Dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Work Directory
WORKDIR /app

# 4. Upgrade PIP
RUN pip install --upgrade pip

# 5. Install PyTorch (CPU Only)
# We do this separately to use the special CPU index URL
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Copy Requirements
COPY requirements.txt .

# 7. Install Dependencies (Robust Mode)
# We use --no-cache-dir to ensure we don't use broken cached wheels
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy Application Code
COPY . .

# 9. Start Command
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]