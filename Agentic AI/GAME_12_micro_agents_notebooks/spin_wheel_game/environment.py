from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

from . import action
from .memory import load_memory, save_memory, public_state


@dataclass
class Environment:
    """E — Environment

    Bridges pure action logic with the outside world:
    - owns the mutable memory dict
    - persists it to disk
    - exposes small high-level operations for the Game + UI.
    """

    memory: Dict[str, Any]

    @classmethod
    def from_disk(cls) -> "Environment":
        return cls(load_memory())

    # M — Memory side
    # ------------------------------------------------------------------
    def snapshot(self) -> Dict[str, Any]:
        """Return a read-only JSON-safe view for the UI."""
        return public_state(self.memory)

    def persist(self) -> None:
        save_memory(self.memory)

    # A — Actions exposed to the Game / UI
    # ------------------------------------------------------------------
    def apply_task_command(self, command: str) -> Dict[str, Any]:
        """Run a text command (add/remove/favorite/hate/list) against tasks."""
        message = action.manage_tasks(self.memory, command)
        self.persist()
        return {
            "message": message,
            "state": self.snapshot(),
        }

    def spin_wheel(self) -> Dict[str, Any]:
        """Pick the next task according to the biased policy."""
        task, count = action.pick_task_biased(self.memory)
        # Remember the last spin for the dashboard.
        self.memory["last_spin"] = {"task": task, "count": count}
        self.persist()

        state = self.snapshot()
        return {
            "task": task,
            "count": count,
            "state": state,
        }

    def record_completion(self, task: str, response: str) -> Dict[str, Any]:
        """Update stats based on whether the user finished / skipped."""
        feedback = action.handle_completion(self.memory, task, response)
        self.persist()
        return {
            "feedback": feedback,
            "state": self.snapshot(),
        }

