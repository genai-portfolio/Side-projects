from __future__ import annotations
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, render_template, request
from decision_agent_game.game import Game
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR/"templates"), static_folder=str(BASE_DIR/"static"))

@app.route("/")
def index(): return render_template("index.html", game=Game.from_disk().view())
@app.route("/api/state")
def api_state(): return jsonify(Game.from_disk().view())
@app.route("/api/decide", methods=["POST"])
def api_decide():
    p = request.get_json(force=True, silent=True) or {}
    oa = (p.get("option_a") or "").strip(); ob = (p.get("option_b") or "").strip()
    if not oa or not ob: return jsonify({"error":"Both options required"}), 400
    sa = p.get("scores_a", {}); sb = p.get("scores_b", {}); w = p.get("weights")
    return jsonify(Game.from_disk().decide(oa, ob, sa, sb, w))
if __name__ == "__main__": app.run(debug=True)
