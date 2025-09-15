# CUDA 12.4 + cuDNN 8 Runtime + Ubuntu 22.04
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
# FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04


# System + Python 3.11 + ffmpeg + tini
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip \
    ffmpeg tini \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3.11 -m pip install --upgrade pip setuptools wheel \
 && python3.11 -m pip install --no-cache-dir -r requirements.txt

# Download script for whisper model
COPY download_whisper.py .
RUN python3.11 download_whisper.py

COPY app ./app
RUN mkdir -p /data/audio

ENV WHISPER_MODEL=medium \
    WHISPER_DEVICE=cuda

EXPOSE 8000
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["python3.11","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
