from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, render_template, request
from reminder_agent_game.game import Game
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR/"templates"), static_folder=str(BASE_DIR/"static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())
@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())
@app.route("/api/set", methods=["POST"])
def api_set():
    p = request.get_json(force=True, silent=True) or {}
    minutes = int(p.get("minutes", 0)); task = (p.get("task") or "").strip()
    if minutes <= 0 or not task: return jsonify({"error":"minutes and task required"}), 400
    return jsonify(Game.from_disk().set_reminder(minutes, task))
@app.route("/api/poll", methods=["POST"])
def api_poll(): return jsonify(Game.from_disk().poll())
if __name__ == "__main__": app.run(debug=True)
