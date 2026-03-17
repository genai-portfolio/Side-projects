from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, render_template, request
from assignment_breakdown_game.game import Game
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR/"templates"), static_folder=str(BASE_DIR/"static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())
@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())
@app.route("/api/step", methods=["POST"])
def api_step():
    p = request.get_json(force=True, silent=True) or {}
    desc = (p.get("description") or "").strip()
    if not desc: return jsonify({"error":"description required"}), 400
    return jsonify(Game.from_disk().get_step(desc))
if __name__ == "__main__": app.run(debug=True)
