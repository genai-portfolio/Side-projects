from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from . import action
from .memory import load_memory, save_memory, public_state


@dataclass
class Environment:
    memory: Dict[str, Any]

    @classmethod
    def from_disk(cls) -> "Environment":
        return cls(load_memory())

    def snapshot(self) -> Dict[str, Any]:
        return public_state(self.memory)

    def persist(self) -> None:
        save_memory(self.memory)

    def add_log(self, text: str) -> Dict[str, Any]:
        result = action.add_log(self.memory, text)
        self.persist()
        return {**result, "state": self.snapshot()}
