from board.Pos import Pos

import copy


class Direction:
    """Class to define directions for movement on the board."""

    def __init__(self, delta_row, delta_col):
        self.delta_row = delta_row
        self.delta_col = delta_col


# Define all eight possible directions in Othello
DIRECTIONS = [
    Direction(-1, 0),
    Direction(1, 0),
    Direction(0, -1),
    Direction(0, 1),
    Direction(-1, -1),
    Direction(-1, 1),
    Direction(1, -1),
    Direction(1, 1),
]


class Board:
    """Class to manage the Othello board and its operations."""

    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.board[3][3], self.board[3][4], self.board[4][3], self.board[4][4] = (
            "W",
            "B",
            "B",
            "W",
        )

    def is_within_bounds(self, pos):
        return 0 <= pos.row < 8 and 0 <= pos.col < 8

    def find_player_positions(self, player):
        return [
            Pos(r, c) for r in range(8) for c in range(8) if self.board[r][c] == player
        ]

    def get_all_valid_moves(self, player):
        valid_moves = []
        opponent = self.get_opponent(player)
        for pos in self.find_player_positions(player):
            for dir in DIRECTIONS:
                next_pos = pos + dir
                if (
                    not self.is_within_bounds(next_pos)
                    or self.board[next_pos.row][next_pos.col] != opponent
                ):
                    continue
                while (
                    self.is_within_bounds(next_pos)
                    and self.board[next_pos.row][next_pos.col] == opponent
                ):
                    next_pos += dir
                if (
                    self.is_within_bounds(next_pos)
                    and self.board[next_pos.row][next_pos.col] == None
                ):
                    if next_pos not in valid_moves:
                        valid_moves.append(next_pos)
        return valid_moves

    def make_move(self, pos, player):
        self.board[pos.row][pos.col] = player

    def flip_pieces(self, pos, player):
        opponent = "W" if player == "B" else "B"
        to_flip = []
        for dir in DIRECTIONS:
            pieces = []
            next_pos = pos + dir
            while (
                self.is_within_bounds(next_pos)
                and self.board[next_pos.row][next_pos.col] == opponent
            ):
                pieces.append(next_pos)
                next_pos += dir
            if (
                self.is_within_bounds(next_pos)
                and self.board[next_pos.row][next_pos.col] == player
            ):
                to_flip.extend(pieces)
        for pos in to_flip:
            self.board[pos.row][pos.col] = player

    def get_opponent(self, player):

        return "W" if player == "B" else "B"

    def score(self):
        black_score = sum(row.count("B") for row in self.board)
        white_score = sum(row.count("W") for row in self.board)
        return {"B": black_score, "W": white_score}

    # def score(self):
    #     black_score = sum(row.count("B") for row in self.board)
    #     white_score = sum(row.count("W") for row in self.board)
    #     if black_score > white_score:
    #         return {"B": 1, "W": 0}  # Svart leder
    #     elif white_score > black_score:
    #         return {"B": 0, "W": -1}  # Vit leder
    #     else:
    #         return {"B": 0, "W": 0}  # Lika

    def is_full(self):

        return all(cell is not None for row in self.board for cell in row)

    def result(self, pos, player):
        """Return a new board state after making a move, without modifying the original board."""
        # new_board = copy.deepcopy(self)  # Skapa en separat kopia av brädet
        new_board = Board()
        new_board.board = [
            row[:] for row in self.board
        ]  # Kopierar endast listan, inte hela objektet

        new_board.make_move(pos, player)
        new_board.flip_pieces(pos, player)
        return new_board  # Returnerar ett nytt bräde
