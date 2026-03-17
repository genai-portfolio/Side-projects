from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from .environment import Environment

@dataclass
class Goals:
    title: str = "Notes Cleaner Agent"
    subtitle: str = "Paste messy notes → get clean Markdown."
    rules: List[str] = field(default_factory=lambda: ["Paste a block of text.","Bullets and headings get normalised.","Download the cleaned Markdown.","History is saved."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls) -> "Game": return cls(environment=Environment.from_disk())
    def view(self) -> Dict[str, Any]: return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def clean(self, raw: str) -> Dict[str, Any]: return self.environment.clean(raw)
