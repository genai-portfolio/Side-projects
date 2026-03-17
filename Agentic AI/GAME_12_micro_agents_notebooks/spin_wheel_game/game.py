from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .environment import Environment


@dataclass
class Goals:
    """G — Goals

    High-level description of what this tiny agent is optimising for.
    Kept separate so students can tweak the "game design" without
    touching the lower-level plumbing.
    """

    title: str = "Spin-the-Wheel Study Task Picker"
    subtitle: str = "One 10-minute challenge at a time."
    rules: List[str] = field(
        default_factory=lambda: [
            "Pick one task per loop.",
            "Give a 10-minute challenge.",
            "Track pick counts, completions and skips.",
            "Bias the wheel 90% towards tasks you hate (sorry).",
        ]
    )
    challenge_minutes: int = 10


@dataclass
class Game:
    """Thin GAME wrapper combining Goals + Environment + Memory + Actions."""

    environment: Environment
    goals: Goals = field(default_factory=Goals)

    # Convenience constructor for the web app
    @classmethod
    def from_disk(cls) -> "Game":
        env = Environment.from_disk()
        return cls(environment=env)

    # Read models for the UI
    # ------------------------------------------------------------------
    def view(self) -> Dict[str, Any]:
        """Full snapshot for rendering the dashboard."""
        return {
            "goals": asdict(self.goals),
            "state": self.environment.snapshot(),
        }

    # GAME loop operations
    # ------------------------------------------------------------------
    def spin(self) -> Dict[str, Any]:
        """Spin the wheel once and return the chosen task + updated state."""
        spin_payload = self.environment.spin_wheel()

        task = spin_payload["task"]
        count = spin_payload["count"]
        minutes = self.goals.challenge_minutes

        message = (
            f"→ {task}\n\n"
            f"{minutes} focused minutes!\n"
            f"(picked {count} time{'s' if count != 1 else ''})"
        )

        return {
            "task": task,
            "count": count,
            "message": message,
            "state": spin_payload["state"],
        }

    def command(self, raw_command: str) -> Dict[str, Any]:
        """Run a text-style management command (add/remove/favorite/hate/list)."""
        return self.environment.apply_task_command(raw_command)

    def complete(self, task: str, response: str) -> Dict[str, Any]:
        """Record whether the user completed / skipped the task."""
        result = self.environment.record_completion(task, response)
        return result

