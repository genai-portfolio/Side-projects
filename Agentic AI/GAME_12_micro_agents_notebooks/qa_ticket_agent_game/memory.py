from __future__ import annotations
import json, os, time
from typing import Any, Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "12_qa_ticket_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"tickets": []}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, indent=2, ensure_ascii=False)
    except: pass

def create_ticket(memory, question, topic, tried, expected, actual, urgency="medium"):
    ticket_id = len(memory.get("tickets", [])) + 1
    ticket = {"id": ticket_id, "question": question, "topic": topic, "tried": tried, "expected": expected, "actual": actual, "urgency": urgency, "ts": time.time()}
    # Format the ticket as a readable block
    formatted = f"""## Ticket #{ticket_id}
**Question:** {question}
**Topic:** {topic}
**What I tried:** {tried}
**Expected:** {expected}
**Actual:** {actual}
**Urgency:** {urgency.upper()}"""
    ticket["formatted"] = formatted
    tickets = memory.setdefault("tickets", [])
    tickets.append(ticket)
    memory["tickets"] = tickets[-100:]
    return ticket

def public_state(memory):
    tickets = memory.get("tickets", [])
    counts = {"low": 0, "medium": 0, "high": 0}
    for t in tickets:
        u = t.get("urgency", "medium")
        counts[u] = counts.get(u, 0) + 1
    return {"total_tickets": len(tickets), "urgency_counts": counts, "recent": list(reversed(tickets[-8:]))}
