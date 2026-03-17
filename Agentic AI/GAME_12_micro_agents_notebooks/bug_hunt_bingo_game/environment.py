from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from . import action
from .memory import load_memory, save_memory, public_state

@dataclass
class Environment:
    memory: Dict[str, Any]
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def toggle(self, index: int) -> Dict[str, Any]:
        msg = action.toggle_mark(self.memory, index); self.persist()
        return {"message": msg, "state": self.snapshot()}
    def new_card(self) -> Dict[str, Any]:
        msg = action.new_card(self.memory); self.persist()
        return {"message": msg, "state": self.snapshot()}
