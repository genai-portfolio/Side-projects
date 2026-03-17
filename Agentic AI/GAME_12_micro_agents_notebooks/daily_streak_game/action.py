from __future__ import annotations

from typing import Any, Dict

from .memory import today_key, compute_streak

MILESTONES = {3: "🔥 3-day streak!", 7: "🏆 One week strong!", 14: "⭐ Two weeks!", 30: "👑 One month!", 100: "💎 100 days!"}


def add_log(memory: Dict[str, Any], text: str) -> Dict[str, str]:
    logs = memory.get("logs", [])
    d = today_key()
    logs = [x for x in logs if x.get("date") != d]
    logs.append({"date": d, "text": text.strip()})
    memory["logs"] = logs

    dates = [x["date"] for x in logs]
    streak = compute_streak(dates)
    memory["streak"] = streak
    memory["longest"] = max(int(memory.get("longest", 0)), streak)

    milestone = MILESTONES.get(streak, "")
    if streak >= 1 and not milestone:
        milestone = f"Day {streak} — keep it going! 💪"

    return {
        "message": f"✅ Logged for {d}. Streak: {streak}. Longest: {memory['longest']}.",
        "milestone": milestone,
    }
