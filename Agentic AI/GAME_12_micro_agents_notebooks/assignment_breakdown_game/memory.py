from __future__ import annotations
import json, os, random, time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "11_assignment_memory.json")

STEP_TEMPLATES = {
    "read": "Read the assignment description carefully and highlight key requirements.",
    "research": "Search for 2-3 relevant resources or examples related to the topic.",
    "outline": "Write a quick outline with 3-5 bullet points for your approach.",
    "code": "Write the first 10 lines of boilerplate / setup code.",
    "test": "Write one simple test case to validate the basic requirement.",
    "draft": "Write a rough first paragraph or section for the report.",
    "diagram": "Draw a quick diagram of the architecture or flow.",
    "review": "Re-read what you have and list 2 things to improve.",
}

KEYWORDS = {"code": ["code","implement","build","program","app","function","class","api"],
    "test": ["test","verify","check","validate","debug"],
    "draft": ["write","essay","report","document","paper"],
    "diagram": ["design","architecture","flow","diagram","uml"],
    "research": ["research","study","learn","explore"]}

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"plans": []}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except: pass

def suggest_step(desc):
    desc_lower = desc.lower()
    for key, words in KEYWORDS.items():
        if any(w in desc_lower for w in words):
            return key, STEP_TEMPLATES[key]
    choices = list(STEP_TEMPLATES.items())
    key, step = random.choice(choices)
    return key, step

def breakdown(memory, description):
    key, step = suggest_step(description)
    record = {"description": description[:200], "step_type": key, "step": step, "ts": time.time()}
    plans = memory.setdefault("plans", [])
    plans.append(record)
    memory["plans"] = plans[-50:]
    return record

def public_state(memory):
    plans = memory.get("plans", [])
    return {"total_plans": len(plans), "recent": list(reversed(plans[-8:]))}
