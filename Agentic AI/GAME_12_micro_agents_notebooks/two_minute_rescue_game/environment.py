from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from . import action
from .memory import load_memory, save_memory, public_state


@dataclass
class Environment:
    """E — Environment: bridges action logic with memory persistence."""

    memory: Dict[str, Any]

    @classmethod
    def from_disk(cls) -> "Environment":
        return cls(load_memory())

    def snapshot(self) -> Dict[str, Any]:
        return public_state(self.memory)

    def persist(self) -> None:
        save_memory(self.memory)

    def pick_rescue_script(self) -> Dict[str, Any]:
        script, total_picks = action.pick_script(self.memory)
        self.memory["last_script"] = script["name"]
        self.persist()
        return {
            "script": script,
            "total_picks": total_picks,
            "state": self.snapshot(),
        }

    def record_feedback(self, script_name: str, helped: bool) -> Dict[str, Any]:
        feedback = action.record_feedback(self.memory, script_name, helped)
        self.persist()
        return {
            "feedback": feedback,
            "state": self.snapshot(),
        }
