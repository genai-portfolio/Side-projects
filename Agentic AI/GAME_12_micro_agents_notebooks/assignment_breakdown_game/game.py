from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .memory import load_memory, save_memory, breakdown, public_state

class Environment:
    def __init__(self, memory): self.memory = memory
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def get_step(self, description):
        record = breakdown(self.memory, description); self.persist()
        return {**record, "state": self.snapshot()}

@dataclass
class Goals:
    title: str = "Assignment Breakdown Agent"
    subtitle: str = "Describe your assignment → get the next 10-minute step."
    rules: List[str] = field(default_factory=lambda: ["Describe the assignment.","Get a smart next step.","Steps matched to assignment type.","Plan history is saved."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def get_step(self, desc): return self.environment.get_step(desc)
