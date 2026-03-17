from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .environment import Environment

@dataclass
class Goals:
    title: str = "One-Line Quiz Agent"
    subtitle: str = "Quick quizzes by topic — no answer key, just honest practice."
    rules: List[str] = field(default_factory=lambda: [
        "Pick a topic: Python, DSA, or DB.",
        "Answer in one line — no peeking.",
        "Answers are logged, not graded.",
        "Rate your confidence 1-5.",
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

    def question(self, topic: str) -> Dict[str, Any]:
        return self.environment.get_question(topic)

    def answer(self, topic: str, question: str, answer: str, confidence: int) -> Dict[str, Any]:
        return self.environment.submit_answer(topic, question, answer, confidence)
