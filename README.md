# Reversi (Othello) Web App

A polished, full-stack implementation of the classic **Reversi / Othello** strategy game built with:

- **Python (Flask)** backend  
- **Vanilla HTML / CSS / JavaScript** frontend  
- Modular game engine architecture  
- Multiple AI strategies (Random → Minimax)

The backend is the single source of truth for rules, state transitions, AI decisions, and replay snapshots.  
The browser is responsible for rendering, user interaction, and animations.

---

# Game Overview

Reversi is a classic 8×8 strategy game where players alternate placing discs to capture the opponent’s pieces by bracketing them horizontally, vertically, or diagonally.

This implementation includes:

- Local Player vs Player
- Player vs AI (multiple difficulty levels)
- Move history timeline
- Replay mode using server-side snapshots
- Undo functionality (PvP only)
- Production-style WSGI setup

---

# Screenshots

## Main Menu – Vs Computer Mode

![Main Menu Vs Computer](assets/screenshots/main_menu_vs_computer.png)

- Choose **Vs Computer** or **Local PvP**
- Select player color (Black / White)
- Choose AI difficulty
- Structured setup flow before starting the match

---

## Main Menu – Local PvP Mode with Replay Option

![Main Menu Vs Player](assets/screenshots/main_menue_vs_player.png)

- Local two-player mode
- Optional **Undo & Replay toggle**
- Replay enabled only in PvP to preserve fairness vs AI

---

## Live Game – Vs Computer

![Live Game Vs CPU](assets/screenshots/live_game_vs_cpu.png)

- Real-time score tracking
- Turn indicator
- Difficulty badge display
- Legal move highlights
- Move timeline panel with:
  - Move number
  - Player color
  - Board notation (e.g., C4, E3)
  - Exact flipped-disc count

---

## Live Game – Local PvP

![Live Game PvP](assets/screenshots/live_game_vs_player_no_replay.png)

- Centered board layout
- Animated disc placement and flipping
- Accurate score updates
- Automatic pass handling
- Game-over detection with winner/draw popup

---

## Replay Mode

![Replay Mode](assets/screenshots/replay_screen.png)

Replay mode is powered by server-side board snapshots.

Features:

- Step backward / forward through history
- Full move timeline navigation
- Replay state indicator
- Moves disabled during replay (read-only mode)
- Snapshot-based state consistency

---

# Features

## Core Gameplay

- Classic **Reversi / Othello** rules
- 8×8 board
- Legal move validation
- Automatic pass handling
- Accurate disc flipping logic
- Game-over detection
- Final score computation

## Game Modes

- Local PvP
- Vs Computer (PvA)

## AI Difficulties

- `Easy` → Random legal move
- `Medium` → Greedy corner-biased heuristic
- `Hard` → Minimax (depth 5)

## Timeline & Move Tracking

Each move records:

- Move number
- Player color
- Board coordinate (e.g., `C4`)
- Exact flipped-disc count

## Undo & Replay (Local PvP Only)

- Undo one move at a time
- Enter replay mode
- Step backward / forward
- Replay mode blocks live moves
- Server-managed snapshot consistency

## UI & UX

- Modern dark-green theme
- Responsive layout
- Board highlights for legal moves
- Last-move visual emphasis
- Disc placement and flip animations
- Structured home screen flow

---

# Architecture

```text
Browser UI (HTML / CSS / JS)
        |
        v
Flask API Routes (backend/api)
        |
        v
GameState (backend/engine/game_state.py)
        |
        +--> Board Logic & Flipping (engine/board.py)
        +--> AI Strategies (engine/strategies/)
