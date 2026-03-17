from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Mapping


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
MEMORY_FILE = os.path.join(PROJECT_ROOT, "02_rescue_memory.json")


SCRIPTS_DEFAULT: List[Dict[str, Any]] = [
    {
        "name": "Rubber Duck",
        "steps": [
            "Explain the problem out loud in 3 sentences.",
            "Name the exact input and expected output.",
            "Identify the first point you feel uncertain.",
        ],
    },
    {
        "name": "Minimal Example",
        "steps": [
            "Create the smallest input that triggers the bug.",
            "Remove everything not needed to reproduce it.",
            "Test again with only the minimal case.",
        ],
    },
    {
        "name": "First Error First",
        "steps": [
            "Find the first incorrect value in your trace/output.",
            "Ask: what line produced it?",
            "Check assumptions right before that line.",
        ],
    },
    {
        "name": "Base Case Check",
        "steps": [
            "If recursion: write the base case in plain English.",
            "Test the base case with 1 simple input.",
            "Then test 1 step above base case.",
        ],
    },
    {
        "name": "Print & Probe",
        "steps": [
            "Add ONE print/log at the key decision point.",
            "Run once and observe the value.",
            "Remove the print after learning.",
        ],
    },
]


def _coerce_int(val: Any) -> int:
    try:
        return int(val)
    except Exception:
        return 0


def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            raw = {}
    else:
        raw = {}

    stats_raw = raw.get("stats", {})
    stats: Dict[str, Dict[str, int]] = {}
    for name_key in stats_raw:
        entry = stats_raw[name_key]
        if isinstance(entry, dict):
            stats[name_key] = {
                "helped": _coerce_int(entry.get("helped", 0)),
                "total": _coerce_int(entry.get("total", 0)),
            }

    last_script = raw.get("last_script") or None

    return {
        "stats": stats,
        "last_script": last_script,
    }


def save_memory(memory: Dict[str, Any]) -> None:
    data = {
        "stats": memory.get("stats", {}),
        "last_script": memory.get("last_script"),
    }
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        return


def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    stats = memory.get("stats", {})
    scripts = []
    for s in SCRIPTS_DEFAULT:
        name = s["name"]
        entry = stats.get(name, {"helped": 0, "total": 0})
        helped = _coerce_int(entry.get("helped", 0))
        total = _coerce_int(entry.get("total", 0))
        rate = round(helped / total * 100) if total > 0 else 0
        scripts.append({
            "name": name,
            "steps": s["steps"],
            "helped": helped,
            "total": total,
            "success_rate": rate,
        })

    return {
        "scripts": scripts,
        "last_script": memory.get("last_script"),
        "totals": {
            "helped": sum(s["helped"] for s in scripts),
            "total": sum(s["total"] for s in scripts),
        },
    }
