import random
import copy
from board.board import Board


class AI_adv:
    def __init__(self, player_color, depth=3):
        self.player_color = player_color
        self.depth = depth

    def adversarial_search(self, board):
        temp_board = copy.deepcopy(board)
        current_player = self.player_color
        best_action = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        actions = temp_board.get_all_valid_moves(self.player_color)
        for a in actions:
            new_board = copy.deepcopy(temp_board)
            new_board.result(a, self.player_color)
            score = self.score(new_board, current_player, alpha, beta, self.depth - 1)

            if score > best_score:
                best_score = score
                best_action = a

            alpha = max(alpha, best_score)

        return best_action

    def score(self, temp_board, current_player, alpha, beta, depth):
        return self.min_player(temp_board, current_player, alpha, beta, depth)

    def min_player(self, temp_board, current_player, alpha, beta, depth):
        if temp_board.is_full():
            return temp_board.score()[self.player_color]
        if depth == 0:
            return self.evaluate_board(temp_board)

        actions = temp_board.get_all_valid_moves(current_player)
        best_score = float("inf")

        for a in actions:
            new_board = copy.deepcopy(temp_board)
            new_board.result(a, current_player)

            best_score = min(
                best_score,
                self.max_player(new_board, self.player_color, alpha, beta, depth - 1),
            )

            beta = min(beta, best_score)
            if best_score <= alpha:
                break

        return best_score

    def max_player(self, temp_board, current_player, alpha, beta, depth):
        if temp_board.is_full():
            return temp_board.score()[self.player_color]
        if depth == 0:
            return self.evaluate_board(temp_board)

        actions = temp_board.get_all_valid_moves(self.player_color)
        best_score = float("-inf")

        for a in actions:
            new_board = copy.deepcopy(temp_board)  # Skapa en kopia av brädet
            new_board.result(a, self.player_color)  # Utför draget på kopian

            best_score = max(
                best_score,
                self.min_player(new_board, current_player, alpha, beta, depth - 1),
            )

            alpha = max(alpha, best_score)
            if best_score >= beta:
                break

        return best_score

    def evaluate_board(self, board):
        score = board.score()
        return score[self.player_color] - score[board.get_opponent(self.player_color)]
