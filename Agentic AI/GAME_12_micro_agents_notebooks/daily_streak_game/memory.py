from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "03_streak_memory.json")


def today_key() -> str:
    return time.strftime("%Y-%m-%d")


def compute_streak(dates: List[str]) -> int:
    if not dates:
        return 0
    days = sorted(set(dates))
    t = time.strptime(today_key(), "%Y-%m-%d")
    today_epoch_days = int(time.mktime(t) // 86400)

    streak = 0
    for i in range(0, 3650):
        day_str = time.strftime("%Y-%m-%d", time.localtime((today_epoch_days - i) * 86400))
        if day_str in days:
            streak += 1
        else:
            break
    return streak


def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            raw = {}
    else:
        raw = {}

    logs = raw.get("logs", [])
    if not isinstance(logs, list):
        logs = []

    streak = int(raw.get("streak", 0))
    longest = int(raw.get("longest", 0))

    return {"logs": logs, "streak": streak, "longest": longest}


def save_memory(memory: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception:
        return


def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    logs = memory.get("logs", [])
    dates = [x.get("date", "") for x in logs if isinstance(x, dict)]
    streak = compute_streak(dates)
    longest = max(int(memory.get("longest", 0)), streak)

    # Build calendar data (last 30 days)
    t = time.strptime(today_key(), "%Y-%m-%d")
    today_epoch = int(time.mktime(t) // 86400)
    date_set = set(dates)
    calendar = []
    for i in range(29, -1, -1):
        d = time.strftime("%Y-%m-%d", time.localtime((today_epoch - i) * 86400))
        calendar.append({"date": d, "active": d in date_set})

    # Recent logs (last 10)
    recent = list(reversed(logs[-10:]))

    return {
        "streak": streak,
        "longest": longest,
        "total_days": len(set(dates)),
        "calendar": calendar,
        "recent_logs": recent,
        "today": today_key(),
    }
