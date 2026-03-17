from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .environment import Environment


@dataclass
class Goals:
    """G — Goals"""
    title: str = "2-Minute Rescue Agent"
    subtitle: str = "Stuck? Get a 2-minute debugging script."
    rules: List[str] = field(
        default_factory=lambda: [
            "Pick one rescue script each time.",
            "Follow the 3-step script in under 2 minutes.",
            "Rate whether it helped — stats guide future picks.",
            "Scripts that help more get picked more often.",
        ]
    )


@dataclass
class Game:
    """GAME wrapper: Goals + Environment + Memory + Actions."""

    environment: Environment
    goals: Goals = field(default_factory=Goals)

    @classmethod
    def from_disk(cls) -> "Game":
        env = Environment.from_disk()
        return cls(environment=env)

    def view(self) -> Dict[str, Any]:
        return {
            "goals": asdict(self.goals),
            "state": self.environment.snapshot(),
        }

    def pick_script(self) -> Dict[str, Any]:
        return self.environment.pick_rescue_script()

    def feedback(self, script_name: str, helped: bool) -> Dict[str, Any]:
        return self.environment.record_feedback(script_name, helped)
