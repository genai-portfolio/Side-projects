from __future__ import annotations

from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

from daily_streak_game.game import Game

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
    return render_template("index.html", game=game.view())


@app.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(new_game().view())


@app.route("/api/log", methods=["POST"])
def api_log():
    game = new_game()
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    result = game.log(text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
