from __future__ import annotations
import json, os, time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "10_decision_memory.json")

CRITERIA = ["time", "difficulty", "impact"]
WEIGHTS = {"time": 0.3, "difficulty": 0.3, "impact": 0.4}

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"decisions": []}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except: pass

def decide(memory, option_a, option_b, scores_a, scores_b, weights=None):
    w = weights or WEIGHTS
    sa = sum(w.get(c, 0.33) * scores_a.get(c, 5) for c in CRITERIA)
    sb = sum(w.get(c, 0.33) * scores_b.get(c, 5) for c in CRITERIA)
    winner = option_a if sa >= sb else option_b
    record = {"option_a": option_a, "option_b": option_b, "scores_a": scores_a, "scores_b": scores_b, "score_a": round(sa, 2), "score_b": round(sb, 2), "winner": winner, "ts": time.time()}
    decisions = memory.setdefault("decisions", [])
    decisions.append(record)
    memory["decisions"] = decisions[-50:]
    return record

def public_state(memory):
    decisions = memory.get("decisions", [])
    return {"total_decisions": len(decisions), "recent": list(reversed(decisions[-8:])), "criteria": CRITERIA, "default_weights": WEIGHTS}
