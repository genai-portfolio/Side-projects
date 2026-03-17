from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from pathlib import Path
from flask import Flask, jsonify, render_template, request
import json, os

# Inline environment + game for compactness
from .memory import load_memory, save_memory, get_mentor_response, public_state

class Environment:
    def __init__(self, memory): self.memory = memory
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def mentor(self, progress):
        result = get_mentor_response(self.memory, progress); self.persist()
        return {**result, "state": self.snapshot()}

@dataclass
class Goals:
    title: str = "Tiny Mentor Agent"
    subtitle: str = "Daily progress → praise + micro-challenge."
    rules: List[str] = field(default_factory=lambda: ["Tell what you did today.","Get encouragement + a micro-challenge.","Last 3 challenges won't repeat.","History is saved."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def mentor(self, progress): return self.environment.mentor(progress)
