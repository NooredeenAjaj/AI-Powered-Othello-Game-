import random
import copy
from board.board import Board


class AI_adv:
    def __init__(self, player_color, depth=4):
        self.player_color = player_color
        self.depth = depth

    def adversarial_search(self, board):
        temp_board = copy.deepcopy(board)
        current_player = self.player_color
        best_action = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        actions = temp_board.get_all_valid_moves(current_player)
        print("från advers ")
        print(len(actions))
        if len(actions) == 0:
            return None
        for a in actions:
            new_board = temp_board.result(a, current_player)
            opponent = new_board.get_opponent(current_player)

            score = self.score(new_board, opponent, alpha, beta, self.depth - 1)

            if score > best_score:
                best_score = score
                best_action = a

        return best_action

    def score(self, temp_board, current_player, alpha, beta, depth):
        return self.min_player(temp_board, current_player, alpha, beta, depth)

    def min_player(self, temp_board, current_player, alpha, beta, depth):
        if temp_board.is_full():
            return temp_board.score()[current_player]
        if depth == 0:
            return self.evaluate_board(temp_board)

        actions = temp_board.get_all_valid_moves(current_player)

        best_score = float("inf")

        for a in actions:

            new_board = temp_board.result(a, current_player)
            next_player = new_board.get_opponent(current_player)

            best_score = min(
                best_score,
                self.max_player(new_board, next_player, alpha, beta, depth - 1),
            )

            beta = min(beta, best_score)
            if best_score <= alpha:
                break

        return best_score

    def max_player(self, temp_board, current_player, alpha, beta, depth):
        if temp_board.is_full():
            return temp_board.score()[current_player]
        if depth == 0:
            return self.evaluate_board(temp_board)

        actions = temp_board.get_all_valid_moves(current_player)
        best_score = float("-inf")

        for a in actions:

            new_board = temp_board.result(a, current_player)
            next_player = new_board.get_opponent(current_player)
            best_score = max(
                best_score,
                self.min_player(new_board, next_player, alpha, beta, depth - 1),
            )

            alpha = max(alpha, best_score)
            if best_score >= beta:
                break

        return best_score

    # def evaluate_board(self, board):
    #     score = board.score()
    #     return score[self.player_color] - score[board.get_opponent(self.player_color)]

    # def evaluate_board(self, board):
    #     corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    #     corner_value = 25
    #     edge_value = 5
    #     board_evaluation = 0

    #     for r in range(8):
    #         for c in range(8):
    #             cell_value = 0
    #             if (r, c) in corners:
    #                 cell_value = corner_value
    #             elif r == 0 or r == 7 or c == 0 or c == 7:
    #                 cell_value = edge_value

    #             if board.board[r][c] == self.player_color:
    #                 board_evaluation += cell_value
    #             elif board.board[r][c] == board.get_opponent(self.player_color):
    #                 board_evaluation -= cell_value

    #     # Additional score based on simple piece count
    #     # scores = board.score()
    #     # board_evaluation += (
    #     #     scores[self.player_color] - scores[board.get_opponent(self.player_color)]
    #     # )

    #     return board_evaluation

    def evaluate_board(self, board):
        edges = {(r, c): 5 for r in [0, 7] for c in range(8)} | {
            (r, c): 5 for r in range(8) for c in [0, 7]
        }

        corners = {(r, c): 25 for r in [0, 7] for c in [0, 7]}
        x_squares = {(r, c): -20 for r in [1, 6] for c in [1, 6]}
        c_squares = {(r, c): 10 for r in [0, 7] for c in [1, 6]} | {
            (r, c): 10 for r in [1, 6] for c in [0, 7]
        }
        middle_block = {(r, c): 3 for r in range(2, 6) for c in range(2, 6)}

        position_values = {}

        position_values.update(edges)

        position_values.update(corners)
        # position_values.update(x_squares)
        # position_values.update(c_squares)
        position_values.update(middle_block)

        board_evaluation = 0
        for r in range(8):
            for c in range(8):
                cell_value = position_values.get((r, c), 0)

                if board.board[r][c] == self.player_color:
                    board_evaluation += cell_value
                elif board.board[r][c] == board.get_opponent(self.player_color):
                    board_evaluation -= cell_value

        scores = board.score()
        piece_diff = (
            scores[board.get_opponent(self.player_color)] - scores[self.player_color]
        )
        max_spaces = 64
        remaining_spaces = max_spaces - (
            scores[board.get_opponent(self.player_color)] + scores[self.player_color]
        )
        weight = 1 - (remaining_spaces / max_spaces)
        board_evaluation += weight * piece_diff

        # print(board_evaluation)

        # board_evaluation += (
        #     scores[board.get_opponent(self.player_color)] - scores[self.player_color]
        # )
        return board_evaluation
