from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, render_template, request
from bug_hunt_bingo_game.game import Game
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR/"templates"), static_folder=str(BASE_DIR/"static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())
@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())
@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    p = request.get_json(force=True, silent=True) or {}
    return jsonify(Game.from_disk().toggle(int(p.get("index", 0))))
@app.route("/api/new_card", methods=["POST"])
def api_new(): return jsonify(Game.from_disk().new_card())
if __name__ == "__main__": app.run(debug=True)
