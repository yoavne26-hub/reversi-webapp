import math
import random

from ..board import opponent

WEIGHTS = [
    [130, -30, 30, 6, 6, 30, -30, 130],
    [-30, -60, -6, -6, -6, -6, -60, -30],
    [30, -6, 15, 3, 3, 15, -6, 30],
    [6, -6, 3, 3, 3, 3, -6, 6],
    [6, -6, 3, 3, 3, 3, -6, 6],
    [30, -6, 15, 3, 3, 15, -6, 30],
    [-30, -60, -6, -6, -6, -6, -60, -30],
    [130, -30, 30, 6, 6, 30, -30, 130],
]


def corner_moves(moves):
    return [m for m in [(0, 0), (0, 7), (7, 0), (7, 7)] if m in moves]


def evaluate(board, player):
    val = 0
    opp = opponent(player)
    for r in range(8):
        for c in range(8):
            if board.grid[r][c] == player:
                val += WEIGHTS[r][c]
            elif board.grid[r][c] == opp:
                val -= WEIGHTS[r][c]
    my_moves = len(board.legal_moves(player))
    opp_moves = len(board.legal_moves(opp))
    val += 5 * (my_moves - opp_moves)
    return val


def minimax(board, root_player, depth, alpha, beta, maximizing):
    me = root_player if maximizing else opponent(root_player)
    moves = board.legal_moves(me)

    if depth == 0 or (not moves and not board.legal_moves(opponent(me))):
        return evaluate(board, root_player), None

    best_move = None
    if not moves:
        value, _ = minimax(board, root_player, depth - 1, alpha, beta, not maximizing)
        return value, None

    if maximizing:
        value = -math.inf
        for (r, c), flips in moves.items():
            nb = board.clone()
            nb.apply_move(r, c, me, flips)
            v, _ = minimax(nb, root_player, depth - 1, alpha, beta, False)
            if v > value:
                value, best_move = v, (r, c)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move

    value = math.inf
    for (r, c), flips in moves.items():
        nb = board.clone()
        nb.apply_move(r, c, me, flips)
        v, _ = minimax(nb, root_player, depth - 1, alpha, beta, True)
        if v < value:
            value, best_move = v, (r, c)
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value, best_move


class MinimaxStrategy:
    def __init__(self, depth=4):
        self.depth = depth

    def choose_move(self, board, player):
        moves = board.legal_moves(player)
        if not moves:
            return None
        corners = corner_moves(moves)
        if corners:
            return random.choice(corners)
        _, move = minimax(board, player, self.depth, -math.inf, math.inf, True)
        return move

