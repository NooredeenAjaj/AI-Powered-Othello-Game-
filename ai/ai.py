import random
import copy


class AI:
    def __init__(self, player_color, depth=3):
        self.player_color = player_color
        self.depth = depth  # Djupet för Minimax-sökningen

    def find_best_move(self, board):
        """Return the best move based on Minimax with Alpha-Beta pruning."""
        best_move = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        valid_moves = board.get_all_valid_moves(self.player_color)
        if not valid_moves:
            return None  # Inga giltiga drag

        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            temp_board.make_move(move, self.player_color)
            score = self.minimax(temp_board, self.depth - 1, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)  # Uppdatera Alpha
            if beta <= alpha:
                break  # Beskärning

        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """Recursive Minimax function with Alpha-Beta pruning."""
        if (
            depth == 0
            or not board.get_all_valid_moves(self.player_color)
            and not board.get_all_valid_moves(board.get_opponent(self.player_color))
        ):
            return self.evaluate_board(board)

        if is_maximizing:  # AI:s drag (maximerande)
            max_eval = float("-inf")
            for move in board.get_all_valid_moves(self.player_color):
                temp_board = copy.deepcopy(board)
                temp_board.make_move(move, self.player_color)
                eval = self.minimax(temp_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beskärning
            return max_eval

        else:  # Motståndarens drag (minimerande)
            min_eval = float("inf")
            opponent = board.get_opponent(self.player_color)
            for move in board.get_all_valid_moves(opponent):
                temp_board = copy.deepcopy(board)
                temp_board.make_move(move, opponent)
                eval = self.minimax(temp_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Beskärning
            return min_eval

    def evaluate_board(self, board):
        """Evaluate the board for AI based on piece count."""
        score = board.score()
        return score[self.player_color] - score[board.get_opponent(self.player_color)]
