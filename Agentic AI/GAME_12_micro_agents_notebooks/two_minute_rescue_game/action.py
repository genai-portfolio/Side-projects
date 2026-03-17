from __future__ import annotations

import random
from typing import Any, Dict, Tuple

from .memory import SCRIPTS_DEFAULT


def pick_script(memory: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """Pick a rescue script with smoothed weighting toward more helpful ones."""
    stats = memory.get("stats", {})
    weights = []
    for s in SCRIPTS_DEFAULT:
        name = s["name"]
        d = stats.get(name, {"helped": 0, "total": 0})
        helped = int(d.get("helped", 0))
        total = int(d.get("total", 0))
        weights.append((helped + 1) / (total + 2))  # Laplace smoothing

    idx = random.choices(range(len(SCRIPTS_DEFAULT)), weights=weights, k=1)[0]
    script = SCRIPTS_DEFAULT[idx]
    total_picks = int(stats.get(script["name"], {}).get("total", 0))
    return script, total_picks


def record_feedback(memory: Dict[str, Any], script_name: str, helped: bool) -> str:
    """Record whether a rescue script helped and return feedback message."""
    stats = memory.setdefault("stats", {})
    entry = stats.get(script_name, {"helped": 0, "total": 0})
    entry["total"] = int(entry.get("total", 0)) + 1
    if helped:
        entry["helped"] = int(entry.get("helped", 0)) + 1
    stats[script_name] = entry

    if helped:
        messages = [
            "Great — this approach works for you! 🎯",
            "Nice, adding that to your toolkit! 🛠️",
            "Awesome, rescue successful! 🚀",
        ]
    else:
        messages = [
            "No worries, try a different script next time! 🔄",
            "Not every tool fits every problem. Keep going! 💪",
            "Filed under 'tried it'. On to the next! 📋",
        ]
    return random.choice(messages)
