from __future__ import annotations
import json, os, random
from typing import Any, Dict, List, Set

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "07_bingo_memory.json")

BUGS = ["Off-by-one","Wrong base case","Wrong loop condition","Indentation error","Variable shadowing","Forgot return","Mutating list while iterating","Wrong index","Type mismatch","Uninitialized variable","Wrong comparison","Infinite loop"]

BINGO_LINES = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: pass
    return {}

def save_memory(memory: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception: pass

def ensure_grid(memory: Dict[str, Any]) -> None:
    if "grid" not in memory or not memory["grid"]:
        memory["grid"] = random.sample(BUGS, 9)
    if "marked" not in memory:
        memory["marked"] = []

def check_bingo(marked: List[int]) -> List[List[int]]:
    ms = set(marked)
    return [line for line in BINGO_LINES if all(i+1 in ms for i in line)]

def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    ensure_grid(memory)
    grid = memory["grid"]
    marked = memory.get("marked", [])
    bingo_lines = check_bingo(marked)
    cells = []
    for i, bug in enumerate(grid, 1):
        cells.append({"index": i, "name": bug, "marked": i in marked})
    return {"cells": cells, "marked_count": len(marked), "bingo": len(bingo_lines) > 0, "bingo_lines": bingo_lines, "total_games": memory.get("wins", 0)}
