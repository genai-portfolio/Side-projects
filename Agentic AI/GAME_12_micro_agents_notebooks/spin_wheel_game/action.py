from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from .memory import TASKS_DEFAULT


def _ensure_collections(memory: Dict[str, Any]) -> None:
    """Ensure core collections exist with the right container types."""
    if "tasks" not in memory or not memory["tasks"]:
        memory["tasks"] = TASKS_DEFAULT.copy()

    favorites = memory.get("favorites")
    if not isinstance(favorites, (set, list, tuple)):
        favorites = set()
    memory["favorites"] = set(favorites)

    hated = memory.get("hated")
    if not isinstance(hated, (set, list, tuple)):
        hated = set()
    memory["hated"] = set(hated)

    if "picks" not in memory or not isinstance(memory["picks"], dict):
        memory["picks"] = {}

    stats = memory.get("stats")
    if not isinstance(stats, dict):
        stats = {}
    stats.setdefault("completed", {})
    stats.setdefault("skipped", {})
    memory["stats"] = stats


def show_tasks(memory: Dict[str, Any]) -> List[str]:
    """Return a human-readable description of all tasks and tags."""
    _ensure_collections(memory)
    tasks: List[str] = memory["tasks"]
    favorites = memory["favorites"]
    hated = memory["hated"]

    lines = ["Current tasks:"]
    for t in tasks:
        tag = ""
        if t in favorites:
            tag = " ⭐ favorite"
        if t in hated:
            tag = " 💀 hated"
        lines.append(f"  • {t}{tag}")
    return lines


def manage_tasks(memory: Dict[str, Any], command: str) -> str:
    """Mutate the task list using the original text command protocol."""
    _ensure_collections(memory)

    tasks: List[str] = memory["tasks"]
    favorites = memory["favorites"]
    hated = memory["hated"]

    parts = command.strip().split(maxsplit=1)
    if len(parts) == 0:
        return ""

    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd in ("add", "a"):
        if not arg:
            return "Please provide a task to add."
        if arg in tasks:
            return "Task already exists."
        tasks.append(arg)
        return f"+ Added: {arg}"

    if cmd in ("remove", "rm", "del", "d"):
        if not arg:
            return "Which task to remove?"
        if arg not in tasks:
            return "Task not found."
        tasks.remove(arg)
        favorites.discard(arg)
        hated.discard(arg)
        return f"− Removed: {arg}"

    if cmd in ("favorite", "fav", "love", "like"):
        if not arg:
            return "Which task to favorite?"
        if arg not in tasks:
            return "Task not found."
        favorites.add(arg)
        hated.discard(arg)
        return f"⭐ Favorited: {arg}"

    if cmd in ("hate", "dislike", "avoid"):
        if not arg:
            return "Which task do you hate?"
        if arg not in tasks:
            return "Task not found."
        hated.add(arg)
        favorites.discard(arg)
        return f"💀 Hated: {arg}"

    if cmd in ("list", "ls", "show"):
        return "\n".join(show_tasks(memory))

    return ""


def pick_task_biased(memory: Dict[str, Any]) -> Tuple[str, int]:
    """Pick a task with 90% bias towards 'hated' tasks, 10% towards liked/neutral."""
    _ensure_collections(memory)
    tasks: List[str] = memory["tasks"]
    if not tasks:
        return "No tasks left — add some!", 0

    hated = memory["hated"]
    favorites = memory["favorites"]

    hated_tasks = [t for t in tasks if t in hated]
    preferred = [t for t in tasks if t in favorites]
    neutral = [t for t in tasks if t not in hated]

    if not hated_tasks:
        hated_tasks = tasks

    good_pool = preferred if preferred else neutral or tasks

    # 90% chance to pick from hated, 10% from good/neutral
    if random.random() < 0.90 and hated_tasks:
        task = random.choice(hated_tasks)
    else:
        task = random.choice(good_pool)

    picks = memory.setdefault("picks", {})
    picks[task] = int(picks.get(task, 0) or 0) + 1

    return task, picks[task]


def handle_completion(memory: Dict[str, Any], task: str, response: str) -> str:
    """Record whether the user completed or skipped the task and return feedback."""
    _ensure_collections(memory)
    stats = memory["stats"]
    completed: Dict[str, int] = stats["completed"]
    skipped: Dict[str, int] = stats["skipped"]

    r = response.lower().strip()
    if r in ("y", "yes", "done", "finished", "yep", "completed", "ok"):
        completed[task] = int(completed.get(task, 0) or 0) + 1
        options = [
            "Nice — you actually did it 🏆",
            "Respect. Keep going 🔥",
            "Not bad at all... surprised tbh 😏",
        ]
        return random.choice(options)

    if r in ("n", "no", "skip", "nah", "later", "cant"):
        skipped[task] = int(skipped.get(task, 0) or 0) + 1
        roasts = [
            "Dodging again? I see you 👀",
            "This one was gonna own you anyway right?",
            "Overprepared → Netflix time confirmed 🍿",
            "Task exists → you chose vibes instead",
        ]
        return random.choice(roasts)

    return "Just say yes / no / skip next time bro"

