# app/nlu.py
import datetime, json, pathlib, re
from typing import Optional, Dict, Any, List

_LEXICON_PATH = pathlib.Path(__file__).parent / "materials_lexicon.json"
_MATERIALS: List[str] = []

def load_material_lexicon(path: pathlib.Path = _LEXICON_PATH) -> List[str]:
    global _MATERIALS
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        _MATERIALS = [m.strip().lower() for m in data.get("materials", []) if m.strip()]
        print(f"[NLU] loaded {len(_MATERIALS)} materials from {path}")
    except Exception as e:
        print("[NLU] lexicon load failed:", e)
        _MATERIALS = []
    return _MATERIALS

def _word_to_int(token: str) -> Optional[int]:
    token = token.lower().strip()
    mapping = {"null":0,"eins":1,"ein":1,"eine":1,"einen":1,"zwo":2,"zwei":2,"drei":3,"vier":4,
               "fünf":5,"funf":5,"sechs":6,"sieben":7,"acht":8,"neun":9,"zehn":10,
               "elf":11,"zwölf":12,"zwoelf":12}
    if token.isdigit(): return int(token)
    return mapping.get(token)

def _extract_int(m) -> Optional[int]:
    if not m: return None
    val = m.group(1) if m.lastindex else m.group(0)
    if isinstance(val, str):
        val = val.strip()
        if val.isdigit(): return int(val)
        return _word_to_int(val)
    return None

def _find_material_freephrase(t: str) -> Optional[str]:
    # „von <…> verarbeitet|gefertigt|produziert“ oder „material <…>“
    m1 = re.search(r"von\s+([a-z0-9\-\_\/ ]+?)\s+(?:verarbeitet|gefertigt|produziert)", t)
    if m1: return m1.group(1).strip()
    m2 = re.search(r"material\s+([a-z0-9\-\_\/ ]+)", t)
    if m2: return m2.group(1).strip()
    return None

def _find_material_candidate(t: str) -> Optional[str]:
    # exakte Worttreffer aus Lexikon
    for m in _MATERIALS:
        if re.search(rf"\b{re.escape(m)}\b", t):
            return m
    return None

def parse_de(text: str) -> Dict[str, Any]:
    raw = text
    t = " ".join(text.lower().split())

    m_total = re.search(r"(?:habe|hab|wir haben|es sind|insgesamt)\s+(\d+|eins|eine|ein|zwei|drei|vier|fünf|funf|sechs|sieben|acht|neun|zehn|elf|zwölf|zwoelf)\s+(?:teile|stück|stueck)", t)
    total = _extract_int(m_total)

    m_scrap = re.search(r"(?:davon\s+(?:sind\s+)?)?(\d+|eins|eine|ein|zwei|drei|vier|fünf|funf|sechs|sieben|acht|neun|zehn|elf|zwölf|zwoelf)\s+(?:ausschuss|schlecht|verworfen|defekt)", t)
    scrap = _extract_int(m_scrap)

    mat = _find_material_freephrase(t)
    if not mat:
        mat = _find_material_candidate(t)

    good = max(0, total - scrap) if (total is not None and scrap is not None) else None
    conf_nlu = round((0.3 if total is not None else 0) + (0.3 if scrap is not None else 0) + (0.3 if mat else 0), 2)

    return {
        "material": mat,
        "quantity_total": total,
        "quantity_scrap": scrap,
        "quantity_good": good,
        "unit": "pcs",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "confidence": {"asr": None, "nlu": conf_nlu},
        "raw_text": raw
    }
