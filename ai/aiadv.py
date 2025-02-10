import random
import copy
from board.board import Board


class AI_adv:
    """
    Initializes the AI player.

    :param player_color: The color of the AI player (e.g., black or white).
    :param depth: The depth limit for Minimax search (default is 4).
    """

    def __init__(self, player_color, depth=4):
        self.player_color = player_color
        self.depth = depth

    def adversarial_search(self, board):
        """
        Finds the best possible move using Minimax with Alpha-Beta pruning.

        :param board: The current board state.
        :return: The best move (action) for the AI player.
        """

        current_player = self.player_color
        best_action = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        actions = board.get_all_valid_moves(current_player)
        print("från advers ")
        print(len(actions))
        if len(actions) == 0:
            return None
        for a in actions:
            new_board = board.result(a, current_player)
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
        """
        Represents the maximizing player (AI) in the Minimax algorithm.

        :param temp_board: The temporary board state.
        :param current_player: The player making the move.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param depth: Depth of the search tree.
        :return: The highest possible score from this player's perspective.
        """
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

    def evaluate_board(self, board):
        """
        Evaluates the current board state using a heuristic function.

        :param board: The current board state.
        :return: A numerical evaluation of the board state.
        """
        board_evaluation = self.update_with_heuristic(board)

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

        return board_evaluation

    def update_with_heuristic(self, board):
        position_values = self.heuristic()

        board_evaluation = 0
        for r in range(8):
            for c in range(8):
                cell_value = position_values.get((r, c), 0)

                if board.board[r][c] == self.player_color:
                    board_evaluation += cell_value
                elif board.board[r][c] == board.get_opponent(self.player_color):
                    board_evaluation -= cell_value
        return board_evaluation

    def heuristic(self):
        """
        Defines positional heuristics for different board positions.
        Corners and edges are given higher values as they are strategically stronger.

        :return: A dictionary mapping board positions to their heuristic values.
        """
        edges = {(r, c): 5 for r in [0, 7] for c in range(8)} | {
            (r, c): 5 for r in range(8) for c in [0, 7]
        }

        corners = {(r, c): 25 for r in [0, 7] for c in [0, 7]}

        middle_block = {(r, c): 3 for r in range(2, 6) for c in range(2, 6)}

        position_values = {}

        position_values.update(edges)

        position_values.update(corners)

        position_values.update(middle_block)
        return position_values
