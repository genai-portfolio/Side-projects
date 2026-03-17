from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict
from flask import Flask, jsonify, render_template, request
from flashcard_drill_game.game import Game

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())

@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())

@app.route("/api/draw", methods=["POST"])
def api_draw(): return jsonify(Game.from_disk().draw())

@app.route("/api/rate", methods=["POST"])
def api_rate():
    p: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    return jsonify(Game.from_disk().rate(p.get("question",""), p.get("rating","medium")))

@app.route("/api/add_card", methods=["POST"])
def api_add():
    p: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    q, a = (p.get("q") or "").strip(), (p.get("a") or "").strip()
    if not q or not a: return jsonify({"error":"q and a required"}), 400
    return jsonify(Game.from_disk().add_card(q, a))

if __name__ == "__main__":
    app.run(debug=True)
