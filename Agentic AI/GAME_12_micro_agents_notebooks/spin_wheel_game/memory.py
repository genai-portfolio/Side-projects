from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Mapping


# Path where the small agent stores its state.
#
# We keep using the same filename as the notebook version so that
# students can jump between the notebook agent and the web UI.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
MEMORY_FILE = os.path.join(PROJECT_ROOT, "01_spin_wheel_memory.json")


TASKS_DEFAULT: List[str] = [
    "Revise last lecture notes",
    "Solve 2 easy problems",
    "Rewrite one concept in your own words",
    "Make 5 flashcards",
    "Refactor one function name + variables",
    "Watch one short explanation video (max 10 min)",
    "Teach the concept to an imaginary friend",
]


def _coerce_int_mapping(data: Any) -> Dict[str, int]:
    """Return a plain dict[str, int] from possibly-messy JSON data."""
    if not isinstance(data, Mapping):
        return {}
    out: Dict[str, int] = {}
    for key, value in data.items():
        try:
            out[str(key)] = int(value)
        except Exception:
            # Ignore values that cannot be coerced to int
            continue
    return out


def load_memory() -> Dict[str, Any]:
    """Load agent memory from disk and normalise it into a safe structure.

    In-memory we allow Python sets and dicts for convenience, but on disk
    everything is stored as plain JSON (lists + objects). This helper
    cleans up older / partially-written files as well.
    """
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            raw = {}
    else:
        raw = {}

    tasks = raw.get("tasks") or TASKS_DEFAULT.copy()

    # Favourites / hated are stored as lists in JSON, converted to sets in RAM.
    favorites_raw = raw.get("favorites", [])
    hated_raw = raw.get("hated", [])

    if isinstance(favorites_raw, list):
        favorites = set(str(t) for t in favorites_raw)
    elif isinstance(favorites_raw, set):
        favorites = favorites_raw
    else:
        favorites = set()

    if isinstance(hated_raw, list):
        hated = set(str(t) for t in hated_raw)
    elif isinstance(hated_raw, set):
        hated = hated_raw
    else:
        hated = set()

    picks = _coerce_int_mapping(raw.get("picks", {}))

    stats_raw = raw.get("stats") or {}
    completed = _coerce_int_mapping(stats_raw.get("completed", {}))
    skipped = _coerce_int_mapping(stats_raw.get("skipped", {}))

    last_spin = raw.get("last_spin") or {}
    if not isinstance(last_spin, Mapping):
        last_spin = {}

    memory: Dict[str, Any] = {
        "tasks": list(tasks),
        "favorites": favorites,
        "hated": hated,
        "picks": picks,
        "stats": {
            "completed": completed,
            "skipped": skipped,
        },
        "last_spin": {
            "task": last_spin.get("task"),
            "count": last_spin.get("count", 0),
        },
    }
    return memory


def _serialise_memory(memory: Dict[str, Any]) -> Dict[str, Any]:
    """Convert in-RAM structure into something json.dump can handle."""
    tasks = memory.get("tasks") or TASKS_DEFAULT.copy()
    favorites = memory.get("favorites", set())
    hated = memory.get("hated", set())
    if not isinstance(favorites, (set, list, tuple)):
        favorites = set()
    if not isinstance(hated, (set, list, tuple)):
        hated = set()

    stats = memory.get("stats") or {}
    completed = stats.get("completed", {})
    skipped = stats.get("skipped", {})

    last_spin = memory.get("last_spin") or {}
    if not isinstance(last_spin, Mapping):
        last_spin = {}

    return {
        "tasks": list(tasks),
        "favorites": list(favorites),
        "hated": list(hated),
        "picks": dict(memory.get("picks", {})),
        "stats": {
            "completed": dict(completed),
            "skipped": dict(skipped),
        },
        "last_spin": {
            "task": last_spin.get("task"),
            "count": int(last_spin.get("count", 0) or 0),
        },
    }


def save_memory(memory: Dict[str, Any]) -> None:
    """Persist the current memory snapshot to disk."""
    data = _serialise_memory(memory)
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        # For classroom use we keep this silent; the app can still run
        # with in-process state even if disk writes fail.
        return


def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-safe view for the UI layer.

    This folds the internal dicts/sets into a task-centric list so that
    the front-end can easily render everything without reimplementing
    the bookkeeping logic.
    """
    tasks: List[str] = list(memory.get("tasks") or TASKS_DEFAULT.copy())
    favorites = set(memory.get("favorites", set()))
    hated = set(memory.get("hated", set()))
    picks = memory.get("picks", {})
    stats = memory.get("stats", {})
    completed = stats.get("completed", {})
    skipped = stats.get("skipped", {})

    task_rows = []
    for name in tasks:
        task_rows.append(
            {
                "name": name,
                "favorite": name in favorites,
                "hated": name in hated,
                "picked_count": int(picks.get(name, 0) or 0),
                "completed_count": int(completed.get(name, 0) or 0),
                "skipped_count": int(skipped.get(name, 0) or 0),
            }
        )

    last_spin = memory.get("last_spin") or {}
    if not isinstance(last_spin, Mapping):
        last_spin = {}

    return {
        "tasks": task_rows,
        "last_spin": {
            "task": last_spin.get("task"),
            "count": int(last_spin.get("count", 0) or 0),
        },
        "totals": {
            "completed": sum(int(v or 0) for v in completed.values()),
            "skipped": sum(int(v or 0) for v in skipped.values()),
        },
    }

