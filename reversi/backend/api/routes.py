from flask import Blueprint, jsonify, render_template, request

from ..engine import (
    BLACK,
    WHITE,
    GameState,
    GreedyCornerStrategy,
    MinimaxStrategy,
    RandomStrategy,
)

web_bp = Blueprint("web", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")

STATE = None


def state_or_404():
    global STATE
    if STATE is None:
        return None, (jsonify({"ok": False, "error": "No active game"}), 400)
    return STATE, None


def make_strategy(difficulty):
    if difficulty == "easy":
        return RandomStrategy()
    if difficulty == "medium":
        return GreedyCornerStrategy()
    if difficulty == "hard":
        return MinimaxStrategy(depth=5)
    raise ValueError("Invalid difficulty")


@web_bp.get("/")
def index():
    return render_template("index.html")


@api_bp.post("/new")
def api_new():
    global STATE
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "pva")

    if mode == "pvp":
        STATE = GameState(
            human_color=BLACK,
            ai_strategy=None,
            enable_undo=bool(data.get("enable_undo", False)),
        )
        return jsonify({"ok": True, "state": STATE.as_dict()})

    if mode != "pva":
        return jsonify({"ok": False, "error": "Invalid mode"}), 400

    human_str = str(data.get("human", "black")).lower()
    if human_str not in {"black", "white"}:
        return jsonify({"ok": False, "error": "Invalid human color"}), 400
    human_color = BLACK if human_str == "black" else WHITE

    difficulty = str(data.get("difficulty", "medium")).lower()
    try:
        strategy = make_strategy(difficulty)
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    STATE = GameState(human_color=human_color, ai_strategy=strategy, enable_undo=False)
    return jsonify({"ok": True, "state": STATE.as_dict()})


@api_bp.get("/state")
def api_state():
    state, err = state_or_404()
    if err:
        return err
    return jsonify({"ok": True, "state": state.as_dict()})


@api_bp.post("/move")
def api_move():
    state, err = state_or_404()
    if err:
        return err
    data = request.get_json(silent=True) or {}
    try:
        r = int(data["r"])
        c = int(data["c"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"ok": False, "error": "Body must include integer r and c", "state": state.as_dict()}), 400

    if state.ai_strategy is not None and state.current_player == state.ai_color:
        return jsonify({"ok": False, "error": "It is not the human player's turn", "state": state.as_dict()}), 400
    if state.replay_mode:
        return jsonify({"ok": False, "error": "Cannot play moves in replay mode.", "state": state.as_dict()}), 400

    ok, error = state.apply_move(r, c)
    if not ok:
        return jsonify({"ok": False, "error": error, "state": state.as_dict()}), 400
    return jsonify({"ok": True, "state": state.as_dict()})


@api_bp.post("/ai")
def ai_step():
    state, err = state_or_404()
    if err:
        return err
    if state.ai_strategy is None:
        return jsonify({"ok": False, "error": "AI is not enabled for this game.", "state": state.as_dict()}), 400
    if state.replay_mode:
        return jsonify({"ok": False, "error": "Cannot run AI in replay mode.", "state": state.as_dict()}), 400

    state.apply_ai_if_needed()
    return jsonify({"ok": True, "state": state.as_dict()})


def _undo_replay_guard():
    state, err = state_or_404()
    if err:
        return None, err
    if state.ai_strategy is not None or state.as_dict().get("mode") != "pvp":
        return None, (jsonify({"ok": False, "error": "Undo/Replay is only available in Local PvP.", "state": state.as_dict()}), 400)
    if not state.enable_undo:
        return None, (jsonify({"ok": False, "error": "Undo/Replay is not enabled for this game.", "state": state.as_dict()}), 400)
    return state, None


@api_bp.post("/undo")
def api_undo():
    state, err = _undo_replay_guard()
    if err:
        return err
    if state.replay_mode:
        return jsonify({"ok": False, "error": "Cannot undo while in replay mode.", "state": state.as_dict()}), 400
    ok, error = state.undo_one()
    if not ok:
        return jsonify({"ok": False, "error": error, "state": state.as_dict()}), 400
    return jsonify({"ok": True, "state": state.as_dict()})


@api_bp.post("/replay/enter")
def api_replay_enter():
    state, err = _undo_replay_guard()
    if err:
        return err
    ok, error = state.enter_replay_mode()
    if not ok:
        return jsonify({"ok": False, "error": error, "state": state.as_dict()}), 400
    return jsonify({"ok": True, "state": state.as_dict()})


@api_bp.post("/replay/exit")
def api_replay_exit():
    state, err = _undo_replay_guard()
    if err:
        return err
    ok, error = state.exit_replay_mode()
    if not ok:
        return jsonify({"ok": False, "error": error, "state": state.as_dict()}), 400
    return jsonify({"ok": True, "state": state.as_dict()})


@api_bp.post("/replay/step")
def api_replay_step():
    state, err = _undo_replay_guard()
    if err:
        return err
    if not state.replay_mode:
        return jsonify({"ok": False, "error": "Replay mode is not active.", "state": state.as_dict()}), 400
    data = request.get_json(silent=True) or {}
    ok, error = state.step_replay(data.get("dir"))
    if not ok:
        return jsonify({"ok": False, "error": error, "state": state.as_dict()}), 400
    return jsonify({"ok": True, "state": state.as_dict()})

