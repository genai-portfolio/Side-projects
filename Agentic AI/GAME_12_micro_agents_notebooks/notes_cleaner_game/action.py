from __future__ import annotations
import time
from typing import Any, Dict
from .memory import clean_notes

def process_notes(memory: Dict[str, Any], raw: str) -> Dict[str, str]:
    cleaned = clean_notes(raw)
    history = memory.setdefault("history", [])
    history.append({"ts": time.time(), "input_len": len(raw), "output_len": len(cleaned)})
    memory["history"] = history[-50:]
    return {"cleaned": cleaned, "message": f"✅ Cleaned {len(raw)} chars → {len(cleaned)} chars of Markdown."}
