from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .memory import load_memory, save_memory, decide, public_state

class Environment:
    def __init__(self, memory): self.memory = memory
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def make_decision(self, option_a, option_b, scores_a, scores_b, weights=None):
        result = decide(self.memory, option_a, option_b, scores_a, scores_b, weights); self.persist()
        return {**result, "state": self.snapshot()}

@dataclass
class Goals:
    title: str = "Decision Agent"
    subtitle: str = "Compare two options with weighted criteria."
    rules: List[str] = field(default_factory=lambda: ["Enter two options.","Score each on time, difficulty, impact (1-10).","Adjust weights if needed.","Get a data-backed recommendation."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def decide(self, option_a, option_b, scores_a, scores_b, weights=None): return self.environment.make_decision(option_a, option_b, scores_a, scores_b, weights)
