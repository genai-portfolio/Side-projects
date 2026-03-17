from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from . import action
from .memory import load_memory, save_memory, public_state

@dataclass
class Environment:
    memory: Dict[str, Any]

    @classmethod
    def from_disk(cls) -> "Environment": return cls(load_memory())
    def snapshot(self) -> Dict[str, Any]: return public_state(self.memory)
    def persist(self) -> None: save_memory(self.memory)

    def draw(self) -> Dict[str, Any]:
        card = action.draw_card(self.memory)
        self.persist()
        return {**card, "state": self.snapshot()}

    def rate(self, question: str, rating: str) -> Dict[str, Any]:
        msg = action.rate_card(self.memory, question, rating)
        self.persist()
        return {"message": msg, "state": self.snapshot()}

    def add_card(self, q: str, a: str) -> Dict[str, Any]:
        msg = action.add_card(self.memory, q, a)
        self.persist()
        return {"message": msg, "state": self.snapshot()}
