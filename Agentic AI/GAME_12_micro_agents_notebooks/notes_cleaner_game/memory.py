from __future__ import annotations
import json, os, time, re
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "06_notes_cleaner_memory.json")

def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: pass
    return {"history": []}

def save_memory(memory: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception: pass

def clean_notes(raw: str) -> str:
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    cleaned = []
    n = 1
    for ln in lines:
        # Detect headings (lines ending with ':')
        if ln.endswith(":") and len(ln) < 60:
            cleaned.append(f"\n## {ln.rstrip(':')}\n")
        elif ln.startswith(("-", "*", "•", ">")):
            ln = re.sub(r'^[-*•>]+\s*', '', ln)
            cleaned.append(f"- {ln}")
        else:
            cleaned.append(f"{n}. {ln}")
            n += 1
    return "# Clean Notes\n\n" + "\n".join(cleaned) + "\n"

def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    history = memory.get("history", [])
    return {"total_cleans": len(history), "recent": list(reversed(history[-5:]))}
