from __future__ import annotations
from typing import Any, Dict
from .memory import get_cards, weighted_pick

def draw_card(memory: Dict[str, Any]) -> Dict[str, Any]:
    cards = get_cards(memory)
    idx = weighted_pick(memory)
    card = cards[idx]
    memory["last_card_idx"] = idx
    return {"q": card["q"], "a": card["a"], "index": idx}

def rate_card(memory: Dict[str, Any], question: str, rating: str) -> str:
    if rating not in {"easy", "medium", "hard"}:
        rating = "medium"
    ratings = memory.setdefault("ratings", {})
    r = ratings.get(question, {"easy": 0, "medium": 0, "hard": 0})
    r[rating] = int(r.get(rating, 0)) + 1
    ratings[question] = r
    icons = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    return f"{icons.get(rating, '')} Rated {rating}!"

def add_card(memory: Dict[str, Any], q: str, a: str) -> str:
    cards = get_cards(memory)
    if any(c["q"] == q for c in cards):
        return "Card with this question already exists."
    cards.append({"q": q, "a": a})
    return f"✅ Added card: {q[:40]}…"
