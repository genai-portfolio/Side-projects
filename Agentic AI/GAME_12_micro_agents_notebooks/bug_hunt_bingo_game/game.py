from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .environment import Environment

@dataclass
class Goals:
    title: str = "Bug Hunt Bingo"
    subtitle: str = "Find bugs, mark your card — get a BINGO!"
    rules: List[str] = field(default_factory=lambda: ["3×3 grid of common bugs.","Click to mark when you find that bug.","Get a row, column, or diagonal for BINGO!","Generate a new card anytime."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def toggle(self, index): return self.environment.toggle(index)
    def new_card(self): return self.environment.new_card()
