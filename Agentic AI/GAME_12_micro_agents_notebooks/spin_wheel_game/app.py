from __future__ import annotations

from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

from spin_wheel_game.game import Game


BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


def new_game() -> Game:
    """Create a fresh Game instance backed by the latest on-disk memory."""
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


@app.route("/api/spin", methods=["POST"])
def api_spin():
    game = new_game()
    result = game.spin()
    return jsonify(result)


@app.route("/api/tasks", methods=["POST"])
def api_tasks():
    game = new_game()
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}

    op = (payload.get("operation") or "").strip().lower()
    task = (payload.get("task") or "").strip()

    # Map structured operations into the original text command protocol.
    if op in {"add", "a", "remove", "rm", "del", "d", "favorite", "fav", "love", "like", "hate", "dislike", "avoid"}:
        raw = f"{op} {task}".strip()
    elif op in {"list", "ls", "show"}:
        raw = op
    else:
        raw = (payload.get("command") or "").strip()

    result = game.command(raw)
    return jsonify(result)


@app.route("/api/complete", methods=["POST"])
def api_complete():
    game = new_game()
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    task = (payload.get("task") or "").strip()
    response = (payload.get("response") or "").strip()

    if not task:
        return jsonify({"error": "task is required"}), 400

    result = game.complete(task, response or "skip")
    return jsonify(result)


if __name__ == "__main__":
    # For classroom demos; in production you'd use a real WSGI server.
    app.run(debug=True)

