from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .environment import Environment

@dataclass
class Goals:
    title: str = "Flashcard Drill Agent"
    subtitle: str = "Flip, rate, repeat — hard cards come back more."
    rules: List[str] = field(default_factory=lambda: ["Show one question at a time.", "Flip to reveal the answer.", "Rate: Easy / Medium / Hard.", "Hard cards appear more often."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)

    @classmethod
    def from_disk(cls) -> "Game": return cls(environment=Environment.from_disk())
    def view(self) -> Dict[str, Any]: return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def draw(self) -> Dict[str, Any]: return self.environment.draw()
    def rate(self, question: str, rating: str) -> Dict[str, Any]: return self.environment.rate(question, rating)
    def add_card(self, q: str, a: str) -> Dict[str, Any]: return self.environment.add_card(q, a)
