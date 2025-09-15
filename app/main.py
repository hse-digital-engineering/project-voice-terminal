# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os, time, pathlib, datetime, json

from . import asr
from . import nlu

APP_DIR = pathlib.Path(__file__).parent
AUDIO_DIR = pathlib.Path("/data/audio")

app = FastAPI(title="Voice Terminal Demo")

# Static UI & audio hosting
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static"), html=True), name="static")
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    nlu.load_material_lexicon()   # Read lexicon
    asr.load_model(eager=True)    # Preload model

@app.get("/", response_class=HTMLResponse)
def index():
    return (APP_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": datetime.datetime.utcnow().isoformat() + "Z"}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename:
        ext = ".webm"
    else:
        ext = os.path.splitext(file.filename)[1].lower() or ".webm"
        if ext not in [".webm", ".ogg", ".wav", ".mp3", ".m4a"]:
            ext = ".webm"

    latest_path = AUDIO_DIR / f"latest{ext}"
    tmp_path = AUDIO_DIR / f"tmp_{int(time.time()*1000)}{ext}"
    with tmp_path.open("wb") as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk: break
            out.write(chunk)
    tmp_path.replace(latest_path)
    url = f"/audio/{latest_path.name}?ts={int(time.time())}"
    return JSONResponse({"ok": True, "path": str(latest_path), "url": url, "bytes": latest_path.stat().st_size})

class ProcessResponse(BaseModel):
    ok: bool
    audio_url: Optional[str] = None
    asr_text: Optional[str] = None
    asr_language: Optional[str] = None
    nlu: Optional[Dict[str, Any]] = None

@app.post("/process", response_model=ProcessResponse)
def process_latest():
    candidates = sorted([p for p in AUDIO_DIR.glob("latest.*") if p.is_file()],
                        key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise HTTPException(status_code=404, detail="Keine Aufnahme gefunden. Bitte zuerst aufnehmen.")
    latest = candidates[0]

    # ASR
    text, detected_language, lang_prob = asr.transcribe(str(latest), language="de")

    # NLU
    parsed = nlu.parse_de(text)
    parsed["confidence"]["asr"] = round(lang_prob, 2)

    # JSON
    (AUDIO_DIR / "latest.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")

    return ProcessResponse(
        ok=True,
        audio_url=f"/audio/{latest.name}?ts={int(time.time())}",
        asr_text=text,
        asr_language=detected_language,
        nlu=parsed
    )
