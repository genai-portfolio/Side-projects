from __future__ import annotations
import json, os, random
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "05_flashcards_memory.json")

FLASHCARDS_DEFAULT: List[Dict[str, str]] = [
    {"q": "Define recursion in one line.", "a": "A function calling itself on smaller subproblems until base case."},
    {"q": "What is a stack?", "a": "A LIFO data structure supporting push/pop."},
    {"q": "What is a Python dict?", "a": "A key-value mapping structure (hash table-like)."},
    {"q": "What is a primary key?", "a": "A column (or set) that uniquely identifies each row."},
    {"q": "What is Big-O notation?", "a": "A way to describe the upper bound of time/space complexity."},
    {"q": "What is a linked list?", "a": "A linear collection where each element points to the next."},
]

def load_memory() -> Dict[str, Any]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: pass
    return {"ratings": {}, "cards": [c.copy() for c in FLASHCARDS_DEFAULT]}

def save_memory(memory: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception: pass

def get_cards(memory: Dict[str, Any]) -> List[Dict[str, str]]:
    cards = memory.get("cards")
    if not cards:
        cards = [c.copy() for c in FLASHCARDS_DEFAULT]
        memory["cards"] = cards
    return cards

def weighted_pick(memory: Dict[str, Any]) -> int:
    cards = get_cards(memory)
    ratings = memory.get("ratings", {})
    weights = []
    for c in cards:
        r = ratings.get(c["q"], {"easy": 0, "medium": 0, "hard": 0})
        w = (int(r.get("hard", 0)) + 3) + (int(r.get("medium", 0)) + 1) + max(1, int(r.get("easy", 0)))
        weights.append(w)
    return random.choices(range(len(cards)), weights=weights, k=1)[0]

def public_state(memory: Dict[str, Any]) -> Dict[str, Any]:
    cards = get_cards(memory)
    ratings = memory.get("ratings", {})
    card_list = []
    for c in cards:
        r = ratings.get(c["q"], {"easy": 0, "medium": 0, "hard": 0})
        total = int(r.get("easy",0)) + int(r.get("medium",0)) + int(r.get("hard",0))
        card_list.append({**c, "ratings": r, "total_reviews": total})
    return {"cards": card_list, "total_cards": len(cards), "total_reviews": sum(c["total_reviews"] for c in card_list)}
