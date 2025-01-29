import random


class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    def find_random_valid_move(self, board, is_valid_move):
        """Find and return a random valid move."""
        valid_moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if is_valid_move(board, row, col, self.player_color):
                    valid_moves.append((row, col))

        if valid_moves:
            return random.choice(valid_moves)
        return None

    def make_move(self, board, is_valid_move, make_move):
        """Select and execute a move on the board."""
        move = self.find_random_valid_move(board, is_valid_move)
        if move:
            make_move(board, *move, self.player_color)
            return move
        return None
