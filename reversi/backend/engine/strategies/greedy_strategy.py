import random


def corner_moves(moves):
    return [m for m in [(0, 0), (0, 7), (7, 0), (7, 7)] if m in moves]


class GreedyCornerStrategy:
    def choose_move(self, board, player):
        moves = board.legal_moves(player)
        if not moves:
            return None
        corners = corner_moves(moves)
        if corners:
            return random.choice(corners)
        best_move = None
        best_flips = -1
        for move, flips in moves.items():
            if len(flips) > best_flips:
                best_flips = len(flips)
                best_move = move
        return best_move

