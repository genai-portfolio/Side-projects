from __future__ import annotations

from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

from two_minute_rescue_game.game import Game

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


def new_game() -> Game:
    return Game.from_disk()


@app.route("/")
def index():
    game = new_game()
    snapshot = game.view()
    return render_template("index.html", game=snapshot)


@app.route("/api/state", methods=["GET"])
def api_state():
    game = new_game()
    return jsonify(game.view())


@app.route("/api/pick", methods=["POST"])
def api_pick():
    game = new_game()
    result = game.pick_script()
    return jsonify(result)


@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    game = new_game()
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    script_name = (payload.get("script_name") or "").strip()
    helped = payload.get("helped", False)

    if not script_name:
        return jsonify({"error": "script_name is required"}), 400

    result = game.feedback(script_name, bool(helped))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
