from __future__ import annotations
import random
from typing import Any, Dict
from .memory import ensure_grid, check_bingo, BUGS

def toggle_mark(memory: Dict[str, Any], index: int) -> str:
    ensure_grid(memory)
    marked = memory.setdefault("marked", [])
    if index in marked:
        marked.remove(index)
        return f"Unmarked cell {index}."
    else:
        marked.append(index)
        bingo = check_bingo(marked)
        if bingo:
            memory["wins"] = int(memory.get("wins", 0)) + 1
            return "🎉 BINGO! You got a line!"
        return f"Marked cell {index}."

def new_card(memory: Dict[str, Any]) -> str:
    memory["grid"] = random.sample(BUGS, 9)
    memory["marked"] = []
    return "🆕 New bingo card generated!"
