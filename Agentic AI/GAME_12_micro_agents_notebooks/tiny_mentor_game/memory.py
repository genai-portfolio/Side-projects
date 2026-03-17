from __future__ import annotations
import json, os, random, time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "08_tiny_mentor_memory.json")

PRAISE = ["Consistency beats intensity.","Small wins compound.","Momentum is a force.","You showed up. That matters.","One step at a time wins the race.","Progress, not perfection."]
CHALLENGES = ["Write 2 test cases for your code.","Rename 3 unclear variables.","Explain your solution in 5 lines.","Solve 1 extra easy problem.","Refactor one function into smaller parts.","Comment 3 tricky lines of code.","Draw a diagram of your approach."]

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"last_challenges": [], "logs": []}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except: pass

def get_mentor_response(memory, progress):
    history = memory.get("last_challenges", [])
    praise = random.choice(PRAISE)
    options = [c for c in CHALLENGES if c not in history[-3:]] or CHALLENGES
    challenge = random.choice(options)
    history.append(challenge)
    memory["last_challenges"] = history[-10:]
    logs = memory.setdefault("logs", [])
    logs.append({"progress": progress, "praise": praise, "challenge": challenge, "ts": time.time()})
    memory["logs"] = logs[-50:]
    return {"praise": praise, "challenge": challenge}

def public_state(memory):
    logs = memory.get("logs", [])
    return {"total_sessions": len(logs), "recent": list(reversed(logs[-8:])), "last_challenges": memory.get("last_challenges", [])[-3:]}
