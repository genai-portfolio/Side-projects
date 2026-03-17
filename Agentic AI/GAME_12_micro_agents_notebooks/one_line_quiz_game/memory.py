from __future__ import annotations
import json, os, time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "04_quiz_memory.json")

QUESTION_BANK: Dict[str, List[str]] = {
    "python": [
        "Difference between list and tuple (1 line)?",
        "What does len(some_dict) return?",
        "What does range(3) produce conceptually?",
        "What is a list comprehension?",
        "Difference between == and is?",
    ],
    "dsa": [
        "Define time complexity in one line.",
        "What is an invariant (1 line)?",
        "What does FIFO mean?",
        "What is a balanced binary tree?",
        "When do you use a stack vs a queue?",
    ],
    "db": [
        "What does a primary key guarantee?",
        "What is a foreign key used for?",
        "What is normalization (1 line)?",
        "What does SQL JOIN do?",
        "Difference between WHERE and HAVING?",
    ],
}

def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"attempts": []}

def save_memory(memory: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    attempts = memory.get("attempts", [])
    topics = list(QUESTION_BANK.keys())
    per_topic = {}
    for t in topics:
        per_topic[t] = len([a for a in attempts if a.get("topic") == t])
    return {
        "topics": topics,
        "questions_per_topic": {t: len(qs) for t, qs in QUESTION_BANK.items()},
        "attempt_count": len(attempts),
        "per_topic_count": per_topic,
        "recent": list(reversed(attempts[-10:])),
    }
