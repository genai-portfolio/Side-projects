from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .memory import load_memory, save_memory, create_ticket, public_state

class Environment:
    def __init__(self, memory): self.memory = memory
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def submit_ticket(self, question, topic, tried, expected, actual, urgency):
        ticket = create_ticket(self.memory, question, topic, tried, expected, actual, urgency); self.persist()
        return {"ticket": ticket, "state": self.snapshot()}

@dataclass
class Goals:
    title: str = "Q/A Ticket Agent"
    subtitle: str = "Turn questions into structured help tickets."
    rules: List[str] = field(default_factory=lambda: ["Fill in: question, topic, what you tried.","Add expected vs actual results.","Set urgency level.","Download formatted ticket."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def submit(self, question, topic, tried, expected, actual, urgency="medium"): return self.environment.submit_ticket(question, topic, tried, expected, actual, urgency)
