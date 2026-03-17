from __future__ import annotations
import random, time
from typing import Any, Dict, Optional
from .memory import QUESTION_BANK

def get_question(topic: str) -> Optional[str]:
    qs = QUESTION_BANK.get(topic.lower())
    if not qs:
        return None
    return random.choice(qs)

def log_attempt(memory: Dict[str, Any], topic: str, question: str, answer: str, confidence: int) -> str:
    attempts = memory.setdefault("attempts", [])
    attempts.append({
        "topic": topic,
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "ts": time.time(),
    })
    memory["attempts"] = attempts[-200:]
    return "✅ Answer logged! No checking — review later to self-assess."
