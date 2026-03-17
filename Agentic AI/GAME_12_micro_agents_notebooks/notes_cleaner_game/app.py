from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict
from flask import Flask, jsonify, render_template, request
from notes_cleaner_game.game import Game
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR/"templates"), static_folder=str(BASE_DIR/"static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())
@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())
@app.route("/api/clean", methods=["POST"])
def api_clean():
    p: Dict[str,Any] = request.get_json(force=True, silent=True) or {}
    raw = (p.get("raw") or "").strip()
    if not raw: return jsonify({"error":"raw text required"}), 400
    return jsonify(Game.from_disk().clean(raw))
if __name__ == "__main__": app.run(debug=True)
