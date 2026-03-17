from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict
from flask import Flask, jsonify, render_template, request
from one_line_quiz_game.game import Game

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))

def new_game() -> Game:
    return Game.from_disk()

@app.route("/")
def index():
    return render_template("index.html", game=new_game().view())

@app.route("/api/state")
def api_state():
    return jsonify(new_game().view())

@app.route("/api/question", methods=["POST"])
def api_question():
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    topic = (payload.get("topic") or "").strip()
    return jsonify(new_game().question(topic))

@app.route("/api/answer", methods=["POST"])
def api_answer():
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    return jsonify(new_game().answer(
        payload.get("topic", ""),
        payload.get("question", ""),
        payload.get("answer", ""),
        int(payload.get("confidence", 3)),
    ))

if __name__ == "__main__":
    app.run(debug=True)
