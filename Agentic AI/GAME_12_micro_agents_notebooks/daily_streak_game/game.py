from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .environment import Environment


@dataclass
class Goals:
    title: str = "Daily Streak Agent"
    subtitle: str = "Build a daily study habit — one line at a time."
    rules: List[str] = field(default_factory=lambda: [
        "Write one line per day about what you studied.",
        "Consecutive days build your streak.",
        "Today's entry can be updated anytime.",
        "Milestone messages at 3, 7, 14, 30, 100 days.",
    ])


@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)

    @classmethod
    def from_disk(cls) -> "Game":
        return cls(environment=Environment.from_disk())

    def view(self) -> Dict[str, Any]:
        return {"goals": asdict(self.goals), "state": self.environment.snapshot()}

    def log(self, text: str) -> Dict[str, Any]:
        return self.environment.add_log(text)
