from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from .memory import load_memory, save_memory, add_reminder, check_reminders, public_state

class Environment:
    def __init__(self, memory): self.memory = memory
    @classmethod
    def from_disk(cls): return cls(load_memory())
    def snapshot(self): return public_state(self.memory)
    def persist(self): save_memory(self.memory)
    def set_reminder(self, minutes, task):
        msg = add_reminder(self.memory, minutes, task); self.persist()
        return {"message": msg, "state": self.snapshot()}
    def poll(self):
        fired = check_reminders(self.memory); self.persist()
        return {"fired": fired, "state": self.snapshot()}

@dataclass
class Goals:
    title: str = "Reminder Agent"
    subtitle: str = "Set quick reminders — never miss a task."
    rules: List[str] = field(default_factory=lambda: ["Set minutes + task description.","Countdown runs in browser.","Get notified when time's up.","All reminders saved."])

@dataclass
class Game:
    environment: Environment
    goals: Goals = field(default_factory=Goals)
    @classmethod
    def from_disk(cls): return cls(environment=Environment.from_disk())
    def view(self): return {"goals": asdict(self.goals), "state": self.environment.snapshot()}
    def set_reminder(self, minutes, task): return self.environment.set_reminder(minutes, task)
    def poll(self): return self.environment.poll()
