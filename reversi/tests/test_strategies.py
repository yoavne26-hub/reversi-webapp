from reversi.backend.engine import BLACK, Board
from reversi.backend.engine.strategies import GreedyCornerStrategy, MinimaxStrategy, RandomStrategy


def test_random_strategy_returns_legal_move():
    board = Board()
    move = RandomStrategy().choose_move(board, BLACK)
    assert move in board.legal_moves(BLACK)


def test_greedy_strategy_prefers_corner_when_available():
    board = Board()
    # Construct a simple corner-available board for black.
    board.grid = [[0 for _ in range(8)] for _ in range(8)]
    board.grid[0][1] = -1
    board.grid[0][2] = 1
    move = GreedyCornerStrategy().choose_move(board, BLACK)
    assert move == (0, 0)


def test_minimax_strategy_returns_valid_move():
    board = Board()
    move = MinimaxStrategy(depth=2).choose_move(board, BLACK)
    assert move in board.legal_moves(BLACK)

