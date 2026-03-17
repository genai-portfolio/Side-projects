from __future__ import annotations
import json, os, time
from typing import Any, Dict, List, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "09_reminder_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"reminders": []}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except: pass

def add_reminder(memory, minutes, task):
    reminders = memory.setdefault("reminders", [])
    created = time.time()
    due = created + minutes * 60
    reminders.append({"task": task, "minutes": minutes, "created": created, "due": due, "done": False})
    memory["reminders"] = reminders[-50:]
    return f"⏰ Reminder set: {minutes} min → {task}"

def check_reminders(memory):
    now = time.time()
    reminders = memory.get("reminders", [])
    fired = []
    for r in reminders:
        if not r.get("done") and now >= r.get("due", 0):
            r["done"] = True
            fired.append(r["task"])
    return fired

def public_state(memory):
    now = time.time()
    reminders = memory.get("reminders", [])
    active = [r for r in reminders if not r.get("done")]
    history = [r for r in reminders if r.get("done")]
    items = []
    for r in active:
        remaining = max(0, r["due"] - now)
        items.append({**r, "remaining_sec": int(remaining)})
    return {"active": items, "history": list(reversed(history[-10:])), "total_set": len(reminders), "total_done": len(history)}
