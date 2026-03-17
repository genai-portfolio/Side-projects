from __future__ import annotations

"""
Launcher so you can run the app with:

    cd spin_wheel_game
    python app1.py

It wires up the package context so that relative imports work.
"""

from pathlib import Path
import sys


if __name__ == "__main__" and __package__ is None:
    # Add the parent directory (which contains the `spin_wheel_game` package)
    # to sys.path and mark this module as part of that package so that
    # `from .app import app` succeeds when executed as a script.
    parent = Path(__file__).resolve().parent.parent
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
    __package__ = "spin_wheel_game"

from .app import app


if __name__ == "__main__":
    # Run the Spin-the-Wheel GAME web app
    app.run(debug=True)

