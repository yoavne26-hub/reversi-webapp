from reversi.backend.engine import BLACK, GameState


def test_turn_switches_after_move():
    state = GameState(ai_strategy=None)
    ok, err = state.apply_move(2, 3)
    assert ok and err is None
    assert state.current_player == -BLACK


def test_undo_restores_previous_snapshot():
    state = GameState(ai_strategy=None, enable_undo=True)
    state.apply_move(2, 3)
    state.apply_move(2, 2)
    assert len(state.snapshots) == 3
    ok, err = state.undo_one()
    assert ok and err is None
    assert len(state.snapshots) == 2
    view = state.as_dict()
    assert view["replay_mode"] is False
    assert view["score"] == {"black": 4, "white": 1}


def test_replay_mode_blocks_moves_and_steps_snapshots():
    state = GameState(ai_strategy=None, enable_undo=True)
    state.apply_move(2, 3)
    state.apply_move(2, 2)
    ok, _ = state.enter_replay_mode()
    assert ok
    assert state.as_dict()["replay_mode"] is True
    ok, _ = state.step_replay("back")
    assert ok
    assert state.as_dict()["replay_index"] == 1
    ok, error = state.apply_move(4, 5)
    assert not ok
    assert "replay mode" in error.lower()
    ok, _ = state.exit_replay_mode()
    assert ok
    assert state.as_dict()["replay_mode"] is False

