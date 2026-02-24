# Reversi (Othello) Web App

A polished browser-based Reversi game built with a Python backend (Flask) and a vanilla HTML/CSS/JavaScript frontend. The rules, board logic, and AI run in Python; the browser is responsible for rendering, controls, and animations.

## Screenshots

- Home / Setup screen (placeholder)
- Game screen (board + HUD + timeline) (placeholder)
- Replay mode / win modal (placeholder)

## Features

- Classic **Reversi / Othello** rules on an 8x8 board
- **Local PvP** mode
- **Vs Computer (PvA)** mode
- AI difficulties:
  - `Easy` (Random)
  - `Medium` (Greedy Corner strategy)
  - `Hard` (Minimax, depth 5)
- Automatic pass handling when a player has no legal moves
- Accurate score tracking and game-over detection
- Move timeline panel:
  - move number
  - player color
  - move notation (`C4`, `F5`, etc.)
  - exact flipped-disc count
- Last-move board highlight
- Animated disc placement + flip effects
- Win celebration popup (winner/draw + final score + actions)
- Optional **Undo + Replay Mode** (Local PvP only):
  - Undo one move at a time
  - Replay timeline using server-side snapshots
  - Step backward / forward through snapshots
  - Replay mode blocks moves (read-only)
- Professional UI:
  - Home screen setup flow
  - Centered board layout
  - Responsive behavior
  - Replay mode visual cues

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **WSGI (production-style local run)**: Waitress
- **Tests**: pytest

## Architecture (ASCII)

```text
Browser UI (HTML/CSS/JS)
        |
        v
Flask Routes / API (reversi/backend/api/routes.py)
        |
        v
GameState (reversi/backend/engine/game_state.py)
        |
        +--> Board rules + flips (reversi/backend/engine/board.py)
        +--> AI strategies (reversi/backend/engine/strategies/*)
```

## Repository Layout

```text
reversi/
  backend/
    api/
    engine/
  frontend/
    static/
    templates/
  tests/
  docs/
run.py
wsgi.py
requirements.txt
start_game.bat
```

## Installation

```bash
pip install -r requirements.txt
```

## Run (Windows One-Click)

Double-click:

- `Play Reversi.bat`

This single launcher will:

1. Install/update dependencies from `requirements.txt` (if needed)
2. Start the app with **Waitress** (WSGI) in a separate terminal window
3. Open the game automatically in your default browser at:
   - `http://127.0.0.1:5000/`

To stop the server, close the `Reversi Server` terminal window (or press `Ctrl+C` in it).

### Make it look nicer (Desktop shortcut with icon)

Batch files (`.bat`) cannot have a custom icon directly.

When you run `Play Reversi.bat`, it now automatically creates/updates a Desktop shortcut:

- `Play Reversi.lnk`

The shortcut includes a generated Reversi-style icon and launches the same one-click flow.

## Run (Command Line)

### Development (Flask dev server)

```bash
python run.py
```

This is best for development/debugging. Flask will show a development-server warning (expected).

### Production-style local run (Waitress WSGI)

```bash
python -m waitress --listen=127.0.0.1:5000 wsgi:app
```

## Testing

```bash
python -m pytest reversi/tests
```

## API Endpoints

- `POST /api/new`
- `GET /api/state`
- `POST /api/move`
- `POST /api/ai`
- `POST /api/undo`
- `POST /api/replay/enter`
- `POST /api/replay/exit`
- `POST /api/replay/step`

Detailed request/response examples:

- `reversi/docs/api.md`

## Documentation

- `reversi/docs/architecture.md` - engine/API/frontend design and state flow
- `reversi/docs/api.md` - endpoint contract and examples

## Deployment Notes

- `run.py` uses Flask's built-in development server (good for local dev, not production)
- `wsgi.py` exposes a WSGI app for production servers
- For Windows deployment, **Waitress** is the simplest option
- For Linux deployment, Gunicorn + reverse proxy (e.g. Nginx) is common

## Future Roadmap

- Save/load games
- Sound effects and richer end-game effects (confetti, themes)
- Online multiplayer
- Bot-vs-bot spectator mode
- More test coverage (engine edge cases + API integration)
- Performance tuning / AI optimizations

## Current Status

- Playable end-to-end locally
- Modular project structure (backend / frontend / tests / docs)
- WSGI entry point included (`wsgi.py`)
- One-click Windows launcher included (`Play Reversi.bat`)
- Auto-created Desktop shortcut with custom Reversi icon (`Play Reversi.lnk`)
