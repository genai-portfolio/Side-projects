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

    def get_question(self, topic: str) -> Dict[str, Any]:
        q = action.get_question(topic)
        if q is None:
            return {"error": f"Unknown topic. Pick from: {', '.join(self.snapshot()['topics'])}"}
        return {"question": q, "topic": topic}

    def submit_answer(self, topic: str, question: str, answer: str, confidence: int) -> Dict[str, Any]:
        msg = action.log_attempt(self.memory, topic, question, answer, confidence)
        self.persist()
        return {"message": msg, "state": self.snapshot()}
