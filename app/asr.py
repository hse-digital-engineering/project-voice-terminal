# app/asr.py
import os, pathlib, time
from faster_whisper import WhisperModel
from typing import Optional, Tuple, Iterable

_ASR_MODEL = None
_ASR_DEVICE = os.environ.get("WHISPER_DEVICE", "cpu")
_ASR_NAME   = os.environ.get("WHISPER_MODEL", "tiny")
_ASR_LOCAL  = os.environ.get("FASTER_WHISPER_DIR")  # optional: preinstalled model

def _model_ref() -> str:
    p = pathlib.Path(_ASR_LOCAL) if _ASR_LOCAL else None
    return str(p) if p and p.exists() else _ASR_NAME

def load_model(eager: bool = False):
    global _ASR_MODEL
    if _ASR_MODEL is None or eager:
        compute_type = "int8" if _ASR_DEVICE == "cpu" else "float16"
        ref = _model_ref()
        try:
            print(f"[ASR] Loading Whisper: {ref} (device={_ASR_DEVICE}, ct={compute_type})")
            _ASR_MODEL = WhisperModel(ref, device=_ASR_DEVICE, compute_type=compute_type)
        except Exception as e:
            # Fallback on CPU, avoid error 500 if CUDA doesn't work
            print("[ASR] init failed on", _ASR_DEVICE, "→ fallback CPU:", e)
            _ASR_MODEL = WhisperModel(ref, device="cpu", compute_type="int8")
    return _ASR_MODEL

def transcribe(audio_path: str, language: str = "de") -> Tuple[str, str, float]:
    # Returns (Text, detected_language, language_prob)

    model = load_model()
    t0 = time.time()
    segments, info = model.transcribe(audio_path, language=language, vad_filter=True)
    text = "".join(seg.text for seg in segments).strip()
    print(f"[ASR] transcribe {audio_path} -> {len(text)} chars in {time.time()-t0:.2f}s")
    return text, getattr(info, "language", language), float(getattr(info, "language_probability", 1.0))
